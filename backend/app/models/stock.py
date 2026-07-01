from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TrendDirection(str, Enum):
    bullish = "bullish"
    neutral = "neutral"
    bearish = "bearish"


class FactorScore(BaseModel):
    score: float = Field(..., ge=0, le=20, description="Factor score 0-20")
    percentile: float = Field(..., ge=0, le=100)
    label: str
    breakdown: dict[str, float]


class CompositeScore(BaseModel):
    total: float = Field(..., ge=0, le=100)
    grade: str
    percentile: float
    trend: TrendDirection
    bull_probability: float = Field(..., ge=0, le=1)
    bear_probability: float = Field(..., ge=0, le=1)
    neutral_probability: float = Field(..., ge=0, le=1)


class ZenRating(BaseModel):
    ticker: str
    company_name: str
    sector: str
    industry: str
    momentum: FactorScore
    value: FactorScore
    quality: FactorScore
    growth: FactorScore
    risk: FactorScore
    composite: CompositeScore
    last_updated: str
    data_source: str


class PricePoint(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None


class TechnicalIndicators(BaseModel):
    ticker: str
    current_price: float
    price_change_1d: float
    price_change_pct_1d: float
    rsi_14: float
    macd: float
    macd_signal: float
    macd_histogram: float
    bollinger_upper: float
    bollinger_lower: float
    bollinger_mid: float
    atr_14: float
    adx_14: float
    volume_sma_20: int
    current_volume: int
    volume_ratio: float
    price_history: list[PricePoint]
    support_level: float
    resistance_level: float


class Fundamentals(BaseModel):
    ticker: str
    company_name: str
    sector: str
    industry: str
    market_cap: float
    pe_ratio: Optional[float] = None
    forward_pe: Optional[float] = None
    pb_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    ev_ebitda: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    roic: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    revenue_ttm: Optional[float] = None
    revenue_growth_yoy: Optional[float] = None
    eps_ttm: Optional[float] = None
    eps_growth_yoy: Optional[float] = None
    fcf_yield: Optional[float] = None
    dividend_yield: Optional[float] = None
    payout_ratio: Optional[float] = None


class SentimentData(BaseModel):
    ticker: str
    overall_sentiment: float = Field(..., ge=-1, le=1)
    news_sentiment: float = Field(..., ge=-1, le=1)
    social_sentiment: float = Field(..., ge=-1, le=1)
    analyst_consensus: str
    analyst_buy_pct: float
    analyst_hold_pct: float
    analyst_sell_pct: float
    target_price_mean: float
    target_price_high: float
    target_price_low: float
    insider_buying_signal: str
    short_interest_pct: float
    recent_headlines: list[dict]


class RiskMetrics(BaseModel):
    ticker: str
    beta: float
    volatility_30d: float
    volatility_90d: float
    max_drawdown_1y: float
    sharpe_ratio: float
    sortino_ratio: float
    var_95: float
    altman_z_score: Optional[float] = None
    piotroski_f_score: Optional[int] = None
    debt_coverage_ratio: Optional[float] = None
    liquidity_risk: str
    market_risk: str
    overall_risk_level: str
