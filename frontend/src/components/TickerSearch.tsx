'use client';
import { useState, useRef, useEffect } from 'react';
import { Search, X, Loader2 } from 'lucide-react';

const POPULAR_TICKERS = [
  'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META',
  'TSLA', 'JPM', 'JNJ', 'PG', 'XOM', 'V', 'MA', 'BAC', 'WMT',
];

interface TickerSearchProps {
  onSelect: (ticker: string) => void;
  currentTicker?: string;
  loading?: boolean;
}

export function TickerSearch({ onSelect, currentTicker, loading }: TickerSearchProps) {
  const [query, setQuery] = useState('');
  const [open, setOpen] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const filtered = query.length === 0
    ? POPULAR_TICKERS
    : POPULAR_TICKERS.filter(t => t.startsWith(query.toUpperCase()));

  useEffect(() => {
    function handle(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener('mousedown', handle);
    return () => document.removeEventListener('mousedown', handle);
  }, []);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const t = query.trim().toUpperCase();
    if (t && t.length <= 10 && /^[A-Z]+$/.test(t)) {
      onSelect(t);
      setOpen(false);
      setQuery('');
    }
  }

  function handleSelect(ticker: string) {
    onSelect(ticker);
    setQuery('');
    setOpen(false);
    inputRef.current?.blur();
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <form onSubmit={handleSubmit} className="flex items-center gap-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-muted)]" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={e => { setQuery(e.target.value.toUpperCase()); setOpen(true); }}
            onFocus={() => setOpen(true)}
            placeholder="Search ticker (e.g. AAPL)"
            maxLength={10}
            className="input-base w-full pl-9 pr-8 font-mono uppercase tracking-wider"
            aria-label="Stock ticker search"
          />
          {query && (
            <button
              type="button"
              onClick={() => { setQuery(''); inputRef.current?.focus(); }}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-[var(--text-muted)] hover:text-[var(--text)]"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
        <button type="submit" className="btn-primary flex items-center gap-2" disabled={loading}>
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
          Analyze
        </button>
      </form>

      {open && (
        <div className="absolute top-full left-0 mt-1 w-64 card shadow-xl z-50 p-2 animate-fade-in">
          <p className="text-xs text-[var(--text-muted)] px-2 pb-1 font-medium uppercase tracking-wider">
            {query ? 'Matches' : 'Popular'}
          </p>
          {filtered.length === 0 ? (
            <p className="px-2 py-1.5 text-sm text-[var(--text-muted)]">
              Press Enter to analyze &quot;{query}&quot;
            </p>
          ) : (
            filtered.slice(0, 8).map(ticker => (
              <button
                key={ticker}
                onClick={() => handleSelect(ticker)}
                className={`w-full text-left px-2 py-1.5 rounded-lg text-sm font-mono hover:bg-[var(--surface-hover)] transition-colors
                  ${ticker === currentTicker ? 'text-brand-400 font-semibold' : ''}`}
              >
                {ticker}
              </button>
            ))
          )}
        </div>
      )}
    </div>
  );
}
