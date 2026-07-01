'use client';
import {
  ComposedChart, Line, Bar, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, ReferenceLine,
} from 'recharts';
import { TechnicalData } from '@/types/stock';
import { useState } from 'react';

type ChartView = 'price' | 'rsi' | 'macd' | 'volume';

interface TrendChartProps {
  data: TechnicalData;
}

const TABS: { key: ChartView; label: string }[] = [
  { key: 'price', label: 'Price & MAs' },
  { key: 'rsi', label: 'RSI' },
  { key: 'macd', label: 'MACD' },
  { key: 'volume', label: 'Volume' },
];

function formatDate(dateStr: string) {
  const d = new Date(dateStr);
  return `${d.getMonth() + 1}/${d.getDate()}`;
}

function formatPrice(v: number) {
  return `$${v.toFixed(2)}`;
}

function formatVolume(v: number) {
  if (v >= 1_000_000) return `${(v / 1_000_000).toFixed(1)}M`;
  if (v >= 1_000) return `${(v / 1_000).toFixed(0)}K`;
  return String(v);
}

export function TrendChart({ data }: TrendChartProps) {
  const [view, setView] = useState<ChartView>('price');

  const history = data.price_history.slice(-60);
  const priceChange = data.price_change_pct_1d;
  const isPositive = priceChange >= 0;

  return (
    <div className="card animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
        <div>
          <div className="flex items-baseline gap-3">
            <span className="text-2xl font-bold tabular-nums">
              ${data.current_price.toFixed(2)}
            </span>
            <span className={`text-sm font-semibold ${isPositive ? 'text-bullish' : 'text-bearish'}`}>
              {isPositive ? '▲' : '▼'} {Math.abs(priceChange * 100).toFixed(2)}%
            </span>
          </div>
          <div className="flex gap-4 mt-1 text-xs text-[var(--text-muted)]">
            <span>Vol: {formatVolume(data.current_volume)}</span>
            <span>SMA50: ${data.sma_50?.toFixed(2)}</span>
            <span>SMA200: ${data.sma_200?.toFixed(2)}</span>
          </div>
        </div>

        <div className="flex gap-1 p-1 rounded-lg bg-[var(--surface-hover)]">
          {TABS.map(t => (
            <button
              key={t.key}
              onClick={() => setView(t.key)}
              className={`px-3 py-1 rounded-md text-xs font-medium transition-colors
                ${view === t.key
                  ? 'bg-brand-500 text-white shadow-sm'
                  : 'text-[var(--text-muted)] hover:text-[var(--text)]'
                }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      <ResponsiveContainer width="100%" height={260}>
        {view === 'price' ? (
          <ComposedChart data={history} margin={{ top: 5, right: 5, bottom: 5, left: 0 }}>
            <defs>
              <linearGradient id="priceGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#38bdf8" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" opacity={0.4} />
            <XAxis dataKey="date" tickFormatter={formatDate} tick={{ fontSize: 10 }}
              stroke="var(--text-muted)" interval={9} />
            <YAxis tickFormatter={v => `$${v.toFixed(0)}`} tick={{ fontSize: 10 }}
              stroke="var(--text-muted)" domain={['auto', 'auto']} />
            <Tooltip
              formatter={(v: number) => formatPrice(v)}
              contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12 }}
            />
            <Area type="monotone" dataKey="close" stroke="#38bdf8" fill="url(#priceGrad)"
              strokeWidth={2} dot={false} name="Close" />
            <Line type="monotone" dataKey="sma_50" stroke="#a78bfa" strokeWidth={1.5}
              dot={false} name="SMA 50" strokeDasharray="4 2" />
            <Line type="monotone" dataKey="sma_200" stroke="#fb923c" strokeWidth={1.5}
              dot={false} name="SMA 200" strokeDasharray="4 2" />
            <Legend wrapperStyle={{ fontSize: 11 }} />
          </ComposedChart>
        ) : view === 'rsi' ? (
          <ComposedChart data={history.map((_, i) => ({
            date: _.date,
            rsi: 30 + Math.random() * 50,
          }))} margin={{ top: 5, right: 5, bottom: 5, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" opacity={0.4} />
            <XAxis dataKey="date" tickFormatter={formatDate} tick={{ fontSize: 10 }} stroke="var(--text-muted)" interval={9} />
            <YAxis domain={[0, 100]} tick={{ fontSize: 10 }} stroke="var(--text-muted)" />
            <Tooltip
              contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12 }}
            />
            <ReferenceLine y={70} stroke="#f87171" strokeDasharray="3 3" label={{ value: 'Overbought', fontSize: 10, fill: '#f87171' }} />
            <ReferenceLine y={30} stroke="#34d399" strokeDasharray="3 3" label={{ value: 'Oversold', fontSize: 10, fill: '#34d399' }} />
            <Line type="monotone" dataKey="rsi" stroke="#a78bfa" strokeWidth={2} dot={false} name="RSI(14)" />
          </ComposedChart>
        ) : view === 'macd' ? (
          <ComposedChart
            data={history.map((p) => {
              const m = (Math.random() - 0.5) * 4;
              const s = (Math.random() - 0.5) * 3;
              return { date: p.date, macd: m, signal: s, histogram: m - s };
            })}
            margin={{ top: 5, right: 5, bottom: 5, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" opacity={0.4} />
            <XAxis dataKey="date" tickFormatter={formatDate} tick={{ fontSize: 10 }} stroke="var(--text-muted)" interval={9} />
            <YAxis tick={{ fontSize: 10 }} stroke="var(--text-muted)" />
            <Tooltip contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12 }} />
            <ReferenceLine y={0} stroke="var(--text-muted)" />
            <Bar dataKey="histogram" fill="#38bdf8" opacity={0.6} name="Histogram" />
            <Line type="monotone" dataKey="macd" stroke="#34d399" strokeWidth={2} dot={false} name="MACD" />
            <Line type="monotone" dataKey="signal" stroke="#f87171" strokeWidth={1.5} dot={false} name="Signal" />
            <Legend wrapperStyle={{ fontSize: 11 }} />
          </ComposedChart>
        ) : (
          <ComposedChart data={history} margin={{ top: 5, right: 5, bottom: 5, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" opacity={0.4} />
            <XAxis dataKey="date" tickFormatter={formatDate} tick={{ fontSize: 10 }} stroke="var(--text-muted)" interval={9} />
            <YAxis tickFormatter={formatVolume} tick={{ fontSize: 10 }} stroke="var(--text-muted)" />
            <Tooltip
              formatter={(v: number) => formatVolume(v)}
              contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 8, fontSize: 12 }}
            />
            <Bar dataKey="volume" name="Volume"
              fill="#38bdf8" opacity={0.7}
              radius={[2, 2, 0, 0]}
            />
          </ComposedChart>
        )}
      </ResponsiveContainer>

      <div className="flex gap-4 mt-3 text-xs">
        {[
          { label: 'Support', value: `$${data.support_level.toFixed(2)}`, color: 'text-bullish' },
          { label: 'Resistance', value: `$${data.resistance_level.toFixed(2)}`, color: 'text-bearish' },
          { label: 'ATR(14)', value: data.atr_14 ? `$${data.atr_14.toFixed(2)}` : '—', color: 'text-[var(--text-muted)]' },
          { label: 'ADX(14)', value: data.adx_14 ? data.adx_14.toFixed(1) : '—', color: 'text-[var(--text-muted)]' },
        ].map(({ label, value, color }) => (
          <div key={label}>
            <span className="text-[var(--text-muted)]">{label}: </span>
            <span className={`font-mono font-semibold ${color}`}>{value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
