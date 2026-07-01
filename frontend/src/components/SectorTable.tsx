'use client';
import { WatchlistItem, TrendDirection } from '@/types/stock';
import { clsx } from 'clsx';
import { useState } from 'react';
import { ChevronUp, ChevronDown } from 'lucide-react';

interface SectorTableProps {
  items: WatchlistItem[];
  currentTicker?: string;
  onSelect: (ticker: string) => void;
}

type SortKey = 'ticker' | 'sector' | 'composite_score' | 'grade' | 'trend';

function TrendBadge({ trend }: { trend: TrendDirection }) {
  return (
    <span className={clsx('badge', {
      'bg-emerald-500/15 text-emerald-400': trend === 'bullish',
      'bg-red-500/15 text-red-400': trend === 'bearish',
      'bg-amber-500/15 text-amber-400': trend === 'neutral',
    })}>
      {trend === 'bullish' ? '▲' : trend === 'bearish' ? '▼' : '—'} {trend}
    </span>
  );
}

function GradeBadge({ grade }: { grade: string }) {
  const color =
    grade.startsWith('A') ? 'bg-emerald-500/15 text-emerald-400' :
    grade.startsWith('B') ? 'bg-brand-500/15 text-brand-400' :
    grade.startsWith('C') ? 'bg-amber-500/15 text-amber-400' :
    'bg-red-500/15 text-red-400';
  return <span className={clsx('badge font-mono', color)}>{grade}</span>;
}

export function SectorTable({ items, currentTicker, onSelect }: SectorTableProps) {
  const [sortKey, setSortKey] = useState<SortKey>('composite_score');
  const [asc, setAsc] = useState(false);
  const [sectorFilter, setSectorFilter] = useState('All');

  const sectors = ['All', ...Array.from(new Set(items.map(i => i.sector))).sort()];

  const filtered = items.filter(i => sectorFilter === 'All' || i.sector === sectorFilter);
  const sorted = [...filtered].sort((a, b) => {
    const av = a[sortKey];
    const bv = b[sortKey];
    if (typeof av === 'number' && typeof bv === 'number') return asc ? av - bv : bv - av;
    return asc
      ? String(av).localeCompare(String(bv))
      : String(bv).localeCompare(String(av));
  });

  function toggleSort(key: SortKey) {
    if (sortKey === key) setAsc(!asc);
    else { setSortKey(key); setAsc(false); }
  }

  function SortIcon({ col }: { col: SortKey }) {
    if (sortKey !== col) return null;
    return asc ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />;
  }

  const headers: Array<{ key: SortKey; label: string; align?: string }> = [
    { key: 'ticker', label: 'Ticker' },
    { key: 'sector', label: 'Sector' },
    { key: 'composite_score', label: 'Score', align: 'text-right' },
    { key: 'grade', label: 'Grade', align: 'text-center' },
    { key: 'trend', label: 'Trend', align: 'text-center' },
  ];

  return (
    <div className="card animate-fade-in">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-[var(--text)]">Market Watchlist</h2>
        <select
          value={sectorFilter}
          onChange={e => setSectorFilter(e.target.value)}
          className="input-base py-1 text-xs"
        >
          {sectors.map(s => <option key={s}>{s}</option>)}
        </select>
      </div>

      <div className="overflow-x-auto scrollbar-thin">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-[var(--border)]">
              {headers.map(h => (
                <th
                  key={h.key}
                  onClick={() => toggleSort(h.key)}
                  className={clsx(
                    'py-2 px-2 text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider cursor-pointer select-none',
                    'hover:text-[var(--text)] transition-colors',
                    h.align || 'text-left'
                  )}
                >
                  <span className="inline-flex items-center gap-1">
                    {h.label}
                    <SortIcon col={h.key} />
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.map(item => (
              <tr
                key={item.ticker}
                onClick={() => onSelect(item.ticker)}
                className={clsx(
                  'border-b border-[var(--border)] cursor-pointer transition-colors',
                  'hover:bg-[var(--surface-hover)]',
                  item.ticker === currentTicker && 'bg-brand-500/10 hover:bg-brand-500/15'
                )}
              >
                <td className="py-2 px-2">
                  <span className="font-mono font-bold text-brand-400">{item.ticker}</span>
                </td>
                <td className="py-2 px-2 text-[var(--text-muted)] text-xs">{item.sector}</td>
                <td className="py-2 px-2 text-right">
                  <ScoreBar score={item.composite_score} />
                </td>
                <td className="py-2 px-2 text-center">
                  <GradeBadge grade={item.grade} />
                </td>
                <td className="py-2 px-2 text-center">
                  <TrendBadge trend={item.trend} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function ScoreBar({ score }: { score: number }) {
  const color =
    score >= 80 ? '#34d399' :
    score >= 65 ? '#38bdf8' :
    score >= 50 ? '#fb923c' :
    '#f87171';

  return (
    <div className="flex items-center justify-end gap-2">
      <div className="w-16 h-1.5 rounded-full bg-[var(--border)] overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${score}%`, backgroundColor: color }} />
      </div>
      <span className="font-mono font-semibold text-xs w-6 text-right" style={{ color }}>
        {Math.round(score)}
      </span>
    </div>
  );
}
