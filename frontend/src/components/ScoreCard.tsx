'use client';
import { FactorScore } from '@/types/stock';
import { clsx } from 'clsx';

interface ScoreCardProps {
  label: string;
  icon: string;
  data: FactorScore;
  color: string;
}

function ScoreArc({ score, max = 20, color }: { score: number; max?: number; color: string }) {
  const pct = Math.min(score / max, 1);
  const r = 36;
  const circ = 2 * Math.PI * r;
  const dashOffset = circ * (1 - pct);
  const gradId = `grad-${color.replace('#', '')}`;

  return (
    <svg className="w-24 h-24 -rotate-90" viewBox="0 0 88 88">
      <defs>
        <linearGradient id={gradId} x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor={color} stopOpacity="0.6" />
          <stop offset="100%" stopColor={color} />
        </linearGradient>
      </defs>
      <circle cx="44" cy="44" r={r} fill="none" strokeWidth="8" stroke="currentColor"
        className="text-[var(--border)] opacity-40" />
      <circle
        cx="44" cy="44" r={r}
        fill="none"
        strokeWidth="8"
        stroke={`url(#${gradId})`}
        strokeDasharray={circ}
        strokeDashoffset={dashOffset}
        strokeLinecap="round"
        style={{ transition: 'stroke-dashoffset 0.8s cubic-bezier(0.4,0,0.2,1)' }}
      />
    </svg>
  );
}

const SCORE_COLORS: Record<string, string> = {
  Momentum: '#38bdf8',
  Value: '#a78bfa',
  Quality: '#34d399',
  Growth: '#fb923c',
  Risk: '#f87171',
};

export function ScoreCard({ label, icon, data, color }: ScoreCardProps) {
  const pct = Math.round((data.score / 20) * 100);
  const arcColor = SCORE_COLORS[label] || color;

  const breakdownEntries = Object.entries(data.breakdown)
    .filter(([, v]) => v !== null && v !== undefined)
    .slice(0, 4);

  return (
    <div className="card hover:shadow-md transition-shadow animate-fade-in">
      <div className="flex items-start justify-between mb-3">
        <div>
          <span className="text-xl">{icon}</span>
          <h3 className="text-sm font-semibold text-[var(--text)] mt-1">{label}</h3>
          <p className="text-xs text-[var(--text-muted)] mt-0.5">{data.label}</p>
        </div>
        <div className="relative flex items-center justify-center">
          <ScoreArc score={data.score} color={arcColor} />
          <div className="absolute inset-0 flex flex-col items-center justify-center rotate-90">
            <span className="text-xl font-bold" style={{ color: arcColor }}>
              {data.score.toFixed(1)}
            </span>
            <span className="text-xs text-[var(--text-muted)]">/20</span>
          </div>
        </div>
      </div>

      <div className="mb-3">
        <div className="flex justify-between text-xs text-[var(--text-muted)] mb-1">
          <span>Percentile</span>
          <span className="font-semibold" style={{ color: arcColor }}>{pct}th</span>
        </div>
        <div className="h-1.5 rounded-full bg-[var(--border)] overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-700"
            style={{ width: `${pct}%`, backgroundColor: arcColor }}
          />
        </div>
      </div>

      {breakdownEntries.length > 0 && (
        <div className="space-y-1 border-t border-[var(--border)] pt-2 mt-2">
          {breakdownEntries.map(([key, val]) => (
            <div key={key} className="flex justify-between items-center text-xs">
              <span className="text-[var(--text-muted)] capitalize">
                {key.replace(/_/g, ' ')}
              </span>
              <span className="font-mono font-semibold text-[var(--text)]">
                {typeof val === 'number' ? val.toFixed(1) : '—'}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export function CompositeScoreCard({
  total,
  grade,
  trend,
  bull_probability,
  bear_probability,
  neutral_probability,
}: {
  total: number;
  grade: string;
  trend: string;
  bull_probability: number;
  bear_probability: number;
  neutral_probability: number;
}) {
  const gradeColor =
    total >= 80 ? '#34d399' :
    total >= 65 ? '#38bdf8' :
    total >= 50 ? '#fb923c' :
    '#f87171';

  const trendClass =
    trend === 'bullish' ? 'text-bullish' :
    trend === 'bearish' ? 'text-bearish' :
    'text-neutral-trend';

  const trendIcon =
    trend === 'bullish' ? '▲' :
    trend === 'bearish' ? '▼' :
    '—';

  return (
    <div className="card gradient-score col-span-full lg:col-span-2 animate-fade-in">
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
        <div className="flex flex-col items-center">
          <div
            className="text-6xl font-bold tabular-nums"
            style={{ color: gradeColor }}
          >
            {Math.round(total)}
          </div>
          <div className="text-sm text-[var(--text-muted)] mt-1">/ 100 Composite</div>
          <div
            className="mt-2 text-3xl font-bold rounded-lg px-3 py-1 border-2"
            style={{ color: gradeColor, borderColor: gradeColor + '44' }}
          >
            {grade}
          </div>
        </div>

        <div className="flex-1 space-y-4">
          <div className="flex items-center gap-2">
            <span className={clsx('text-2xl font-bold', trendClass)}>
              {trendIcon}
            </span>
            <span className={clsx('text-lg font-semibold capitalize', trendClass)}>
              {trend} Trend
            </span>
            <span className="badge bg-[var(--surface-hover)] text-[var(--text-muted)] ml-auto">
              Data-driven estimate
            </span>
          </div>

          <div>
            <p className="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider mb-2">
              30-Day Directional Probability
            </p>
            <div className="flex gap-3">
              {[
                { label: 'Bull', prob: bull_probability, color: '#34d399' },
                { label: 'Neutral', prob: neutral_probability, color: '#fb923c' },
                { label: 'Bear', prob: bear_probability, color: '#f87171' },
              ].map(({ label, prob, color }) => (
                <div key={label} className="flex-1 text-center">
                  <div className="text-xl font-bold tabular-nums" style={{ color }}>
                    {Math.round(prob * 100)}%
                  </div>
                  <div className="text-xs text-[var(--text-muted)]">{label}</div>
                  <div className="h-1 mt-1 rounded-full bg-[var(--border)] overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-700"
                      style={{ width: `${prob * 100}%`, backgroundColor: color }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <p className="text-xs text-[var(--text-muted)] italic">
            ⚠ Probability estimates are algorithmic, not financial advice. Past patterns do not guarantee future results.
          </p>
        </div>
      </div>
    </div>
  );
}
