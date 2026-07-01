"""
Real data adapter layer. Falls back to mock data if API keys are not configured.
Plug in your preferred provider (Alpha Vantage, Polygon, Finnhub, or yfinance).
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class RealDataAdapter:
    def __init__(self, settings):
        self.settings = settings
        self._yf = None

    def _get_yfinance(self):
        if self._yf is None:
            try:
                import yfinance as yf
                import os
                cache_dir = os.path.join(os.environ.get("HOME", "/tmp"), ".cache", "py-yfinance")
                os.makedirs(cache_dir, exist_ok=True)
                yf.set_tz_cache_location(cache_dir)
                self._yf = yf
            except ImportError:
                logger.warning("yfinance not installed — install it with: pip install yfinance")
        return self._yf

    def get_fundamentals(self, ticker: str) -> Optional[dict]:
        yf = self._get_yfinance()
        if yf is None:
            return None
        try:
            t = yf.Ticker(ticker)
            info = t.info
            return {
                "ticker": ticker.upper(),
                "company_name": info.get("longName", ticker),
                "sector": info.get("sector", "Unknown"),
                "industry": info.get("industry", "Unknown"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "pb_ratio": info.get("priceToBook"),
                "ps_ratio": info.get("priceToSalesTrailing12Months"),
                "ev_ebitda": info.get("enterpriseToEbitda"),
                "debt_to_equity": info.get("debtToEquity"),
                "current_ratio": info.get("currentRatio"),
                "quick_ratio": info.get("quickRatio"),
                "roe": info.get("returnOnEquity"),
                "roa": info.get("returnOnAssets"),
                "roic": None,
                "gross_margin": info.get("grossMargins"),
                "operating_margin": info.get("operatingMargins"),
                "net_margin": info.get("profitMargins"),
                "revenue_ttm": info.get("totalRevenue"),
                "revenue_growth_yoy": info.get("revenueGrowth"),
                "eps_ttm": info.get("trailingEps"),
                "eps_growth_yoy": info.get("earningsGrowth"),
                "fcf_yield": None,
                "dividend_yield": info.get("dividendYield"),
                "payout_ratio": info.get("payoutRatio"),
                "piotroski_f_score": None,
            }
        except Exception as e:
            logger.error(f"yfinance fundamentals error for {ticker}: {e}")
            return None

    def get_technicals(self, ticker: str) -> Optional[dict]:
        yf = self._get_yfinance()
        if yf is None:
            return None
        try:
            from datetime import date, timedelta
            t = yf.Ticker(ticker)
            end = date.today()
            start = end - timedelta(days=400)
            hist = t.history(start=start.isoformat(), end=end.isoformat())
            if hist.empty:
                hist = t.history(period="6mo")
            if hist.empty:
                logger.warning(f"yfinance: no price data for {ticker}, using mock fallback")
                return None

            closes = hist["Close"]
            volumes = hist["Volume"]
            current_price = float(closes.iloc[-1])
            prev_price = float(closes.iloc[-2])

            sma_50 = float(closes.tail(50).mean()) if len(closes) >= 50 else None
            sma_200 = float(closes.tail(200).mean()) if len(closes) >= 200 else None

            delta = closes.diff()
            gain = delta.clip(lower=0).rolling(14).mean()
            loss = (-delta.clip(upper=0)).rolling(14).mean()
            rs = gain / loss
            rsi = float(100 - (100 / (1 + rs.iloc[-1])))

            ema_12 = closes.ewm(span=12).mean()
            ema_26 = closes.ewm(span=26).mean()
            macd_line = ema_12 - ema_26
            signal_line = macd_line.ewm(span=9).mean()
            macd = float(macd_line.iloc[-1])
            macd_signal = float(signal_line.iloc[-1])

            vol_sma_20 = int(volumes.tail(20).mean())
            curr_vol = int(volumes.iloc[-1])

            bb_mid = float(closes.tail(20).mean())
            bb_std = float(closes.tail(20).std())

            price_history = []
            for idx, row in hist.tail(90).iterrows():
                price_history.append({
                    "date": idx.date().isoformat(),
                    "open": round(float(row["Open"]), 2),
                    "high": round(float(row["High"]), 2),
                    "low": round(float(row["Low"]), 2),
                    "close": round(float(row["Close"]), 2),
                    "volume": int(row["Volume"]),
                })

            return {
                "ticker": ticker.upper(),
                "current_price": round(current_price, 2),
                "price_change_1d": round(current_price - prev_price, 2),
                "price_change_pct_1d": round((current_price - prev_price) / prev_price, 4),
                "rsi_14": round(rsi, 1),
                "macd": round(macd, 3),
                "macd_signal": round(macd_signal, 3),
                "macd_histogram": round(macd - macd_signal, 3),
                "bollinger_upper": round(bb_mid + 2 * bb_std, 2),
                "bollinger_lower": round(bb_mid - 2 * bb_std, 2),
                "bollinger_mid": round(bb_mid, 2),
                "atr_14": None,
                "adx_14": None,
                "volume_sma_20": vol_sma_20,
                "current_volume": curr_vol,
                "volume_ratio": round(curr_vol / vol_sma_20, 2) if vol_sma_20 > 0 else 1.0,
                "sma_50": round(sma_50, 2) if sma_50 else None,
                "sma_200": round(sma_200, 2) if sma_200 else None,
                "price_history": price_history,
                "support_level": round(float(closes.tail(30).min()), 2),
                "resistance_level": round(float(closes.tail(30).max()), 2),
            }
        except Exception as e:
            logger.error(f"yfinance technicals error for {ticker}: {e}")
            return None

    def get_sentiment(self, ticker: str) -> Optional[dict]:
        return None

    def get_risk(self, ticker: str) -> Optional[dict]:
        yf = self._get_yfinance()
        if yf is None:
            return None
        try:
            t = yf.Ticker(ticker)
            info = t.info
            hist = t.history(period="1y")
            if hist.empty:
                return None

            closes = hist["Close"]
            daily_returns = closes.pct_change().dropna()
            vol_30d = float(daily_returns.tail(30).std() * (252 ** 0.5))
            vol_90d = float(daily_returns.tail(90).std() * (252 ** 0.5))

            cumulative = (1 + daily_returns).cumprod()
            rolling_max = cumulative.cummax()
            drawdown = (cumulative - rolling_max) / rolling_max
            max_drawdown = float(drawdown.min())

            debt_eq = info.get("debtToEquity")
            if debt_eq:
                debt_eq = debt_eq / 100

            return {
                "ticker": ticker.upper(),
                "beta": info.get("beta", 1.0),
                "volatility_30d": round(vol_30d, 4),
                "volatility_90d": round(vol_90d, 4),
                "max_drawdown_1y": round(max_drawdown, 4),
                "sharpe_ratio": None,
                "sortino_ratio": None,
                "var_95": round(float(daily_returns.quantile(0.05)), 4),
                "altman_z_score": None,
                "piotroski_f_score": None,
                "debt_coverage_ratio": None,
                "liquidity_risk": "Unknown",
                "market_risk": "High" if (info.get("beta") or 1) > 1.5 else "Moderate",
                "overall_risk_level": "Unknown",
                "debt_to_equity": debt_eq,
            }
        except Exception as e:
            logger.error(f"yfinance risk error for {ticker}: {e}")
            return None
