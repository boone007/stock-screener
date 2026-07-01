import random
import math
from datetime import date, timedelta

TICKERS = {
    "AAPL": {"name": "Apple Inc.", "sector": "Technology", "industry": "Consumer Electronics"},
    "MSFT": {"name": "Microsoft Corporation", "sector": "Technology", "industry": "Software"},
    "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology", "industry": "Internet Services"},
    "AMZN": {"name": "Amazon.com Inc.", "sector": "Consumer Cyclical", "industry": "E-Commerce"},
    "NVDA": {"name": "NVIDIA Corporation", "sector": "Technology", "industry": "Semiconductors"},
    "META": {"name": "Meta Platforms Inc.", "sector": "Technology", "industry": "Social Media"},
    "TSLA": {"name": "Tesla Inc.", "sector": "Consumer Cyclical", "industry": "Auto Manufacturers"},
    "JPM": {"name": "JPMorgan Chase & Co.", "sector": "Financial", "industry": "Banks"},
    "JNJ": {"name": "Johnson & Johnson", "sector": "Healthcare", "industry": "Pharmaceuticals"},
    "PG": {"name": "Procter & Gamble Co.", "sector": "Consumer Defensive", "industry": "Household Products"},
    "XOM": {"name": "Exxon Mobil Corp.", "sector": "Energy", "industry": "Oil & Gas"},
    "BAC": {"name": "Bank of America Corp.", "sector": "Financial", "industry": "Banks"},
    "WMT": {"name": "Walmart Inc.", "sector": "Consumer Defensive", "industry": "Discount Stores"},
    "V": {"name": "Visa Inc.", "sector": "Financial", "industry": "Credit Services"},
    "MA": {"name": "Mastercard Inc.", "sector": "Financial", "industry": "Credit Services"},
}

SECTOR_PE = {
    "Technology": 28,
    "Consumer Cyclical": 22,
    "Financial": 14,
    "Healthcare": 20,
    "Consumer Defensive": 24,
    "Energy": 12,
}

random.seed(42)


def _seed(ticker: str) -> random.Random:
    rng = random.Random()
    rng.seed(hash(ticker) % (2**32))
    return rng


def get_mock_fundamentals(ticker: str) -> dict:
    info = TICKERS.get(ticker.upper(), {
        "name": f"{ticker.upper()} Corp.",
        "sector": "Technology",
        "industry": "Software",
    })
    rng = _seed(ticker)

    sector = info["sector"]
    base_pe = SECTOR_PE.get(sector, 20)

    return {
        "ticker": ticker.upper(),
        "company_name": info["name"],
        "sector": sector,
        "industry": info["industry"],
        "market_cap": rng.uniform(10e9, 3000e9),
        "pe_ratio": rng.uniform(base_pe * 0.5, base_pe * 2.0),
        "forward_pe": rng.uniform(base_pe * 0.4, base_pe * 1.5),
        "pb_ratio": rng.uniform(1.0, 15.0),
        "ps_ratio": rng.uniform(0.5, 20.0),
        "ev_ebitda": rng.uniform(8.0, 40.0),
        "debt_to_equity": rng.uniform(0.0, 3.0),
        "current_ratio": rng.uniform(0.8, 4.0),
        "quick_ratio": rng.uniform(0.5, 3.0),
        "roe": rng.uniform(0.05, 0.45),
        "roa": rng.uniform(0.02, 0.25),
        "roic": rng.uniform(0.05, 0.35),
        "gross_margin": rng.uniform(0.15, 0.75),
        "operating_margin": rng.uniform(0.05, 0.35),
        "net_margin": rng.uniform(0.03, 0.30),
        "revenue_ttm": rng.uniform(5e9, 500e9),
        "revenue_growth_yoy": rng.uniform(-0.10, 0.60),
        "eps_ttm": rng.uniform(1.0, 20.0),
        "eps_growth_yoy": rng.uniform(-0.20, 0.80),
        "fcf_yield": rng.uniform(0.01, 0.12),
        "dividend_yield": rng.uniform(0, 0.05),
        "payout_ratio": rng.uniform(0, 0.70),
        "piotroski_f_score": rng.randint(3, 9),
    }


def get_mock_technicals(ticker: str) -> dict:
    rng = _seed(ticker + "_tech")
    base_price = rng.uniform(50, 500)
    sma_50 = base_price * rng.uniform(0.85, 1.15)
    sma_200 = base_price * rng.uniform(0.80, 1.20)

    history = _generate_price_history(ticker, base_price, 180)

    return {
        "ticker": ticker.upper(),
        "current_price": round(base_price, 2),
        "price_change_1d": round(rng.uniform(-5, 5), 2),
        "price_change_pct_1d": round(rng.uniform(-0.05, 0.05), 4),
        "rsi_14": round(rng.uniform(25, 75), 1),
        "macd": round(rng.uniform(-5, 5), 3),
        "macd_signal": round(rng.uniform(-5, 5), 3),
        "macd_histogram": round(rng.uniform(-2, 2), 3),
        "bollinger_upper": round(base_price * 1.08, 2),
        "bollinger_lower": round(base_price * 0.92, 2),
        "bollinger_mid": round(base_price, 2),
        "atr_14": round(base_price * rng.uniform(0.01, 0.04), 2),
        "adx_14": round(rng.uniform(15, 50), 1),
        "volume_sma_20": rng.randint(5_000_000, 50_000_000),
        "current_volume": rng.randint(3_000_000, 80_000_000),
        "volume_ratio": round(rng.uniform(0.5, 2.5), 2),
        "sma_50": round(sma_50, 2),
        "sma_200": round(sma_200, 2),
        "price_history": history,
        "support_level": round(base_price * 0.92, 2),
        "resistance_level": round(base_price * 1.08, 2),
    }


def get_mock_sentiment(ticker: str) -> dict:
    rng = _seed(ticker + "_sent")
    overall = rng.uniform(-0.3, 0.8)
    buy_pct = rng.uniform(0.40, 0.80)
    sell_pct = rng.uniform(0.05, 0.25)
    hold_pct = 1.0 - buy_pct - sell_pct

    current_price = rng.uniform(50, 500)
    target_mean = current_price * rng.uniform(1.05, 1.30)

    headlines = [
        {"title": f"{ticker} beats Q3 earnings estimates by 12%", "sentiment": 0.8, "source": "Reuters"},
        {"title": f"Analysts raise {ticker} price target amid strong guidance", "sentiment": 0.7, "source": "Bloomberg"},
        {"title": f"{ticker} expands into new markets with strategic acquisition", "sentiment": 0.5, "source": "WSJ"},
        {"title": f"Macroeconomic headwinds could pressure {ticker} margins", "sentiment": -0.3, "source": "CNBC"},
        {"title": f"{ticker} announces $5B share buyback program", "sentiment": 0.6, "source": "MarketWatch"},
    ]

    return {
        "ticker": ticker.upper(),
        "overall_sentiment": round(overall, 3),
        "news_sentiment": round(overall + rng.uniform(-0.1, 0.1), 3),
        "social_sentiment": round(overall + rng.uniform(-0.15, 0.15), 3),
        "analyst_consensus": "Buy" if buy_pct > 0.60 else ("Hold" if hold_pct > sell_pct else "Sell"),
        "analyst_buy_pct": round(buy_pct, 3),
        "analyst_hold_pct": round(hold_pct, 3),
        "analyst_sell_pct": round(sell_pct, 3),
        "target_price_mean": round(target_mean, 2),
        "target_price_high": round(target_mean * 1.20, 2),
        "target_price_low": round(target_mean * 0.80, 2),
        "insider_buying_signal": rng.choice(["Strong Buy", "Moderate Buy", "Neutral", "Light Sell"]),
        "short_interest_pct": round(rng.uniform(0.01, 0.15), 3),
        "recent_headlines": headlines,
    }


def get_mock_risk(ticker: str) -> dict:
    rng = _seed(ticker + "_risk")
    beta = rng.uniform(0.4, 2.2)
    vol_30d = rng.uniform(0.10, 0.55)
    vol_90d = vol_30d * rng.uniform(0.80, 1.20)
    sharpe = rng.uniform(-0.5, 3.5)
    altman = rng.uniform(1.0, 5.0)
    debt_eq = rng.uniform(0.0, 2.5)

    if vol_30d < 0.20 and beta < 1.0:
        risk_level = "Low"
    elif vol_30d < 0.35 and beta < 1.5:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    return {
        "ticker": ticker.upper(),
        "beta": round(beta, 2),
        "volatility_30d": round(vol_30d, 4),
        "volatility_90d": round(vol_90d, 4),
        "max_drawdown_1y": round(rng.uniform(-0.15, -0.55), 4),
        "sharpe_ratio": round(sharpe, 2),
        "sortino_ratio": round(sharpe * rng.uniform(1.0, 1.6), 2),
        "var_95": round(rng.uniform(0.02, 0.08), 4),
        "altman_z_score": round(altman, 2),
        "piotroski_f_score": rng.randint(3, 9),
        "debt_coverage_ratio": round(rng.uniform(1.5, 8.0), 2),
        "liquidity_risk": rng.choice(["Low", "Moderate", "High"]),
        "market_risk": "High" if beta > 1.5 else ("Moderate" if beta > 1.0 else "Low"),
        "overall_risk_level": risk_level,
        "debt_to_equity": round(debt_eq, 2),
    }


def _generate_price_history(ticker: str, current_price: float, days: int) -> list[dict]:
    rng = _seed(ticker + "_hist")
    prices = []
    price = current_price * rng.uniform(0.75, 0.95)

    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    closing_prices = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:
            daily_return = rng.gauss(0.0003, 0.015)
            price = price * (1 + daily_return)
            price = max(price, 1.0)

            spread = price * rng.uniform(0.005, 0.02)
            high = price + spread
            low = price - spread
            open_price = price + rng.uniform(-spread / 2, spread / 2)
            volume = rng.randint(10_000_000, 80_000_000)

            prices.append({
                "date": current_date.isoformat(),
                "open": round(open_price, 2),
                "high": round(high, 2),
                "low": round(low, 2),
                "close": round(price, 2),
                "volume": volume,
            })
            closing_prices.append(price)

        current_date += timedelta(days=1)

    for i, p in enumerate(prices):
        if i >= 50:
            p["sma_50"] = round(sum(closing_prices[i - 49:i + 1]) / 50, 2)
        if i >= 200:
            p["sma_200"] = round(sum(closing_prices[i - 199:i + 1]) / 200, 2)

    if prices:
        prices[-1]["close"] = current_price

    return prices[-90:]
