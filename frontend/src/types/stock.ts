export type TrendDirection = 'bullish' | 'neutral' | 'bearish';

export interface FactorScore {
  score: number;
  percentile: number;
  label: string;
  breakdown: Record<string, number | null>;
}

export interface CompositeScore {
  total: number;
  grade: string;
  percentile: number;
  trend: TrendDirection;
  bull_probability: number;
  bear_probability: number;
  neutral_probability: number;
}

export interface ZenRating {
  ticker: string;
  company_name: string;
  sector: string;
  industry: string;
  momentum: FactorScore;
  value: FactorScore;
  quality: FactorScore;
  growth: FactorScore;
  risk: FactorScore;
  composite: CompositeScore;
  last_updated: string;
  data_source: string;
  cache_hit?: boolean;
}

export interface PricePoint {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  sma_50?: number;
  sma_200?: number;
}

export interface TechnicalData {
  ticker: string;
  current_price: number;
  price_change_1d: number;
  price_change_pct_1d: number;
  rsi_14: number;
  macd: number;
  macd_signal: number;
  macd_histogram: number;
  bollinger_upper: number;
  bollinger_lower: number;
  bollinger_mid: number;
  atr_14: number;
  adx_14: number;
  volume_sma_20: number;
  current_volume: number;
  volume_ratio: number;
  price_history: PricePoint[];
  support_level: number;
  resistance_level: number;
  sma_50: number;
  sma_200: number;
}

export interface FundamentalsData {
  ticker: string;
  company_name: string;
  sector: string;
  industry: string;
  market_cap: number;
  pe_ratio: number | null;
  forward_pe: number | null;
  pb_ratio: number | null;
  ps_ratio: number | null;
  ev_ebitda: number | null;
  debt_to_equity: number | null;
  current_ratio: number | null;
  roe: number | null;
  roa: number | null;
  gross_margin: number | null;
  operating_margin: number | null;
  net_margin: number | null;
  revenue_growth_yoy: number | null;
  eps_growth_yoy: number | null;
  fcf_yield: number | null;
  dividend_yield: number | null;
}

export interface SentimentData {
  ticker: string;
  overall_sentiment: number;
  news_sentiment: number;
  social_sentiment: number;
  analyst_consensus: string;
  analyst_buy_pct: number;
  analyst_hold_pct: number;
  analyst_sell_pct: number;
  target_price_mean: number;
  target_price_high: number;
  target_price_low: number;
  insider_buying_signal: string;
  short_interest_pct: number;
  recent_headlines: Array<{ title: string; sentiment: number; source: string }>;
}

export interface RiskData {
  ticker: string;
  beta: number;
  volatility_30d: number;
  volatility_90d: number;
  max_drawdown_1y: number;
  sharpe_ratio: number;
  sortino_ratio: number;
  var_95: number;
  altman_z_score: number | null;
  piotroski_f_score: number | null;
  overall_risk_level: string;
}

export interface WatchlistItem {
  ticker: string;
  company_name: string;
  sector: string;
  composite_score: number;
  grade: string;
  trend: TrendDirection;
}
