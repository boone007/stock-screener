'use client';
import { SentimentData } from '@/types/stock';
import { clsx } from 'clsx';

interface ProbabilityIndicatorProps {
  sentiment: SentimentData;
}

function SentimentMeter({ value }: { value: number }) {
  const pct = ((value + 1) / 2) * 100;
  const color = value > 0.3 ? '#34d399' : value < -0.3 ? '#f87171' : '#fb923c';

  return (
    <div>
      <div className="flex justify-between text-xs text-[var(--text-muted)] mb-1">
        <span>Bearish</span>
        <span className="font-semibold" style={{ color }}>{(value * 100).toFixed(0)}</span>
        <span>Bullish</span>
      </div>
      <div className="relative h-3 rounded-full bg-gradient-to-r from-red-500/30 via-amber-500/30 to-emerald-500/30">
        <div
          className="absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full border-2 border-white shadow-md transition-all duration-500"
          style={{ left: `calc(${pct}% - 6px)`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

function AnalystBar({
  buy, hold, sell,
}: { buy: number; hold: number; sell: number }) {
  return (
    <div>
      <div className="flex h-3 rounded-full overflow-hidden">
        <div className="bg-emerald-500 transition-all" style={{ width: `${buy * 100}%` }} />
        <div className="bg-amber-500 transition-all" style={{ width: `${hold * 100}%` }} />
        <div className="bg-red-500 transition-all" style={{ width: `${sell * 100}%` }} />
      </div>
      <div className="flex justify-between text-xs mt-1">
        <span className="text-emerald-400">Buy {(buy * 100).toFixed(0)}%</span>
        <span className="text-amber-400">Hold {(hold * 100).toFixed(0)}%</span>
        <span className="text-red-400">Sell {(sell * 100).toFixed(0)}%</span>
      </div>
    </div>
  );
}

export function ProbabilityIndicator({ sentiment }: ProbabilityIndicatorProps) {
  const consensusColor =
    sentiment.analyst_consensus === 'Buy' ? 'text-bullish' :
    sentiment.analyst_consensus === 'Sell' ? 'text-bearish' :
    'text-neutral-trend';

  return (
    <div className="card animate-fade-in space-y-4">
      <h2 className="text-sm font-semibold text-[var(--text)]">Sentiment & Analyst View</h2>

      <div>
        <p className="text-xs text-[var(--text-muted)] mb-2 uppercase tracking-wider font-semibold">
          Overall Sentiment
        </p>
        <SentimentMeter value={sentiment.overall_sentiment} />
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="bg-[var(--surface-hover)] rounded-lg p-3">
          <p className="text-xs text-[var(--text-muted)]">News</p>
          <SentimentMeter value={sentiment.news_sentiment} />
        </div>
        <div className="bg-[var(--surface-hover)] rounded-lg p-3">
          <p className="text-xs text-[var(--text-muted)]">Social</p>
          <SentimentMeter value={sentiment.social_sentiment} />
        </div>
      </div>

      <div>
        <div className="flex items-center justify-between mb-2">
          <p className="text-xs text-[var(--text-muted)] uppercase tracking-wider font-semibold">
            Analyst Consensus
          </p>
          <span className={clsx('text-sm font-bold', consensusColor)}>
            {sentiment.analyst_consensus}
          </span>
        </div>
        <AnalystBar
          buy={sentiment.analyst_buy_pct}
          hold={sentiment.analyst_hold_pct}
          sell={sentiment.analyst_sell_pct}
        />
      </div>

      <div>
        <p className="text-xs text-[var(--text-muted)] uppercase tracking-wider font-semibold mb-2">
          Price Targets
        </p>
        <div className="grid grid-cols-3 gap-2 text-center">
          {[
            { label: 'Low', value: sentiment.target_price_low, color: '#f87171' },
            { label: 'Mean', value: sentiment.target_price_mean, color: '#38bdf8' },
            { label: 'High', value: sentiment.target_price_high, color: '#34d399' },
          ].map(({ label, value, color }) => (
            <div key={label} className="bg-[var(--surface-hover)] rounded-lg p-2">
              <div className="font-mono font-bold text-sm" style={{ color }}>
                ${value.toFixed(2)}
              </div>
              <div className="text-xs text-[var(--text-muted)]">{label}</div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <p className="text-xs text-[var(--text-muted)] uppercase tracking-wider font-semibold mb-2">
          Additional Signals
        </p>
        <div className="flex flex-wrap gap-2">
          <span className="badge bg-[var(--surface-hover)] text-[var(--text)]">
            Insider: {sentiment.insider_buying_signal}
          </span>
          <span className="badge bg-[var(--surface-hover)] text-[var(--text)]">
            Short: {(sentiment.short_interest_pct * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      <div>
        <p className="text-xs text-[var(--text-muted)] uppercase tracking-wider font-semibold mb-2">
          Recent Headlines
        </p>
        <div className="space-y-1.5">
          {sentiment.recent_headlines.slice(0, 3).map((h, i) => {
            const sentColor = h.sentiment > 0.3 ? '#34d399' : h.sentiment < -0.3 ? '#f87171' : '#fb923c';
            return (
              <div key={i} className="flex items-start gap-2 bg-[var(--surface-hover)] rounded-lg p-2">
                <div className="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0" style={{ backgroundColor: sentColor }} />
                <div className="min-w-0">
                  <p className="text-xs text-[var(--text)] leading-snug truncate">{h.title}</p>
                  <p className="text-xs text-[var(--text-muted)]">{h.source}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
