'use client';
import { useState } from 'react';
import { BarChart2, AlertTriangle } from 'lucide-react';
import { ThemeToggle } from './ThemeToggle';
import { TickerSearch } from './TickerSearch';
import { ScoreCard, CompositeScoreCard } from './ScoreCard';
import { TrendChart } from './TrendChart';
import { SectorTable } from './SectorTable';
import { ProbabilityIndicator } from './ProbabilityIndicator';
import { JsonViewer } from './JsonViewer';
import { useZenRating, useTechnicals, useSentiment, useWatchlist } from '@/hooks/useStockData';

const FACTOR_CONFIG = [
  { key: 'momentum' as const, label: 'Momentum', icon: '⚡', color: '#38bdf8' },
  { key: 'value' as const, label: 'Value', icon: '💎', color: '#a78bfa' },
  { key: 'quality' as const, label: 'Quality', icon: '🏆', color: '#34d399' },
  { key: 'growth' as const, label: 'Growth', icon: '📈', color: '#fb923c' },
  { key: 'risk' as const, label: 'Risk', icon: '🛡', color: '#f87171' },
];

function Skeleton({ className }: { className?: string }) {
  return <div className={`animate-pulse rounded-lg bg-[var(--surface-hover)] ${className}`} />;
}

function ErrorBanner({ message }: { message: string }) {
  return (
    <div className="flex items-center gap-2 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
      <AlertTriangle className="w-4 h-4 flex-shrink-0" />
      {message}
    </div>
  );
}

export function Dashboard() {
  const [ticker, setTicker] = useState<string | null>(null);
  const [jsonTarget, setJsonTarget] = useState<'score' | 'technicals'>('score');

  const { data: rating, error: ratingError, isLoading: ratingLoading } = useZenRating(ticker);
  const { data: technicals, isLoading: techLoading } = useTechnicals(ticker);
  const { data: sentiment } = useSentiment(ticker);
  const { data: watchlist } = useWatchlist();

  const isLoading = ratingLoading || techLoading;

  return (
    <div className="min-h-screen bg-[var(--bg)]">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-[var(--border)] bg-[var(--surface)]/80 backdrop-blur-md">
        <div className="mx-auto max-w-[1600px] px-4 py-3 flex items-center justify-between gap-4">
          <div className="flex items-center gap-2.5 flex-shrink-0">
            <BarChart2 className="w-6 h-6 text-brand-400" />
            <span className="font-bold text-[var(--text)] hidden sm:inline">Zen Screener</span>
          </div>

          <TickerSearch
            onSelect={setTicker}
            currentTicker={ticker ?? undefined}
            loading={isLoading}
          />

          <div className="flex items-center gap-2 flex-shrink-0">
            <span className="badge bg-amber-500/15 text-amber-400 hidden sm:inline-flex">
              Not Financial Advice
            </span>
            <ThemeToggle />
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-[1600px] px-4 py-6 space-y-6">
        {/* Disclaimer */}
        <div className="rounded-lg border border-amber-500/30 bg-amber-500/5 px-4 py-2.5 text-xs text-amber-400">
          ⚠ This dashboard provides data-driven analysis and probability estimates only.
          It is <strong>not financial advice</strong>. Always consult a licensed financial advisor before making investment decisions.
        </div>

        {/* Error state */}
        {ratingError && (
          <ErrorBanner message={`Failed to load data for ${ticker}: ${ratingError.message}`} />
        )}

        {/* Welcome / empty state */}
        {!ticker && (
          <div className="card text-center py-16">
            <BarChart2 className="w-16 h-16 text-brand-400/50 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-[var(--text)] mb-2">
              Zen Multi-Factor Stock Screener
            </h2>
            <p className="text-[var(--text-muted)] text-sm max-w-md mx-auto mb-6">
              Search for any ticker above to run the Zen Rating scoring engine.
              Get Momentum, Value, Quality, Growth, and Risk scores with probability insights.
            </p>
            {watchlist && (
              <div className="flex flex-wrap justify-center gap-2">
                {watchlist.results.slice(0, 8).map(item => (
                  <button
                    key={item.ticker}
                    onClick={() => setTicker(item.ticker)}
                    className="badge bg-[var(--surface-hover)] text-[var(--text)] hover:bg-brand-500/20 hover:text-brand-400 transition-colors py-1.5 px-3 text-sm cursor-pointer"
                  >
                    {item.ticker}
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Loading skeleton */}
        {ticker && isLoading && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {[...Array(7)].map((_, i) => <Skeleton key={i} className="h-40" />)}
          </div>
        )}

        {/* Main content */}
        {ticker && rating && !isLoading && (
          <>
            {/* Company header */}
            <div className="flex flex-wrap items-center gap-3">
              <div>
                <h1 className="text-2xl font-bold text-[var(--text)]">
                  {rating.ticker}
                  <span className="ml-3 text-base font-normal text-[var(--text-muted)]">
                    {rating.company_name}
                  </span>
                </h1>
                <div className="flex gap-2 mt-1">
                  <span className="badge bg-[var(--surface-hover)] text-[var(--text-muted)]">{rating.sector}</span>
                  <span className="badge bg-[var(--surface-hover)] text-[var(--text-muted)]">{rating.industry}</span>
                  <span className="badge bg-[var(--surface-hover)] text-[var(--text-muted)]">
                    Source: {rating.data_source}
                    {rating.cache_hit && ' · cached'}
                  </span>
                </div>
              </div>
            </div>

            {/* Composite score + factor cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
              <CompositeScoreCard
                total={rating.composite.total}
                grade={rating.composite.grade}
                trend={rating.composite.trend}
                bull_probability={rating.composite.bull_probability}
                bear_probability={rating.composite.bear_probability}
                neutral_probability={rating.composite.neutral_probability}
              />
              {FACTOR_CONFIG.map(cfg => (
                <ScoreCard
                  key={cfg.key}
                  label={cfg.label}
                  icon={cfg.icon}
                  color={cfg.color}
                  data={rating[cfg.key]}
                />
              ))}
            </div>

            {/* Chart + Sentiment row */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
              <div className="lg:col-span-2">
                {technicals
                  ? <TrendChart data={technicals} />
                  : <Skeleton className="h-80" />
                }
              </div>
              <div>
                {sentiment
                  ? <ProbabilityIndicator sentiment={sentiment} />
                  : <Skeleton className="h-80" />
                }
              </div>
            </div>

            {/* Watchlist table + JSON viewer row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {watchlist && (
                <SectorTable
                  items={watchlist.results}
                  currentTicker={ticker}
                  onSelect={setTicker}
                />
              )}

              <div className="space-y-3">
                <div className="flex gap-2">
                  {(['score', 'technicals'] as const).map(t => (
                    <button
                      key={t}
                      onClick={() => setJsonTarget(t)}
                      className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors capitalize
                        ${jsonTarget === t
                          ? 'bg-brand-500 text-white'
                          : 'bg-[var(--surface-hover)] text-[var(--text-muted)] hover:text-[var(--text)]'
                        }`}
                    >
                      {t}
                    </button>
                  ))}
                </div>
                <JsonViewer
                  data={jsonTarget === 'score' ? rating : technicals}
                  title={jsonTarget === 'score' ? 'Zen Rating JSON' : 'Technicals JSON'}
                />
              </div>
            </div>
          </>
        )}

        {/* Watchlist when no ticker selected */}
        {!ticker && watchlist && (
          <SectorTable
            items={watchlist.results}
            onSelect={setTicker}
          />
        )}
      </main>

      <footer className="border-t border-[var(--border)] mt-12 py-4 text-center text-xs text-[var(--text-muted)]">
        Zen Stock Screener · For informational purposes only · Not financial advice ·
        Data may be delayed or simulated
      </footer>
    </div>
  );
}
