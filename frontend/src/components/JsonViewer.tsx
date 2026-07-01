'use client';
import { useState } from 'react';
import { Copy, Check, ChevronDown, ChevronRight } from 'lucide-react';

interface JsonViewerProps {
  data: unknown;
  title?: string;
}

function JsonNode({ value, depth = 0 }: { value: unknown; depth?: number }) {
  const [collapsed, setCollapsed] = useState(depth > 1);

  if (value === null) return <span className="text-red-400">null</span>;
  if (typeof value === 'boolean') return <span className="text-amber-400">{String(value)}</span>;
  if (typeof value === 'number') return <span className="text-emerald-400">{value}</span>;
  if (typeof value === 'string') return <span className="text-brand-300">&quot;{value}&quot;</span>;

  if (Array.isArray(value)) {
    if (value.length === 0) return <span className="text-[var(--text-muted)]">[]</span>;
    return (
      <span>
        <button onClick={() => setCollapsed(!collapsed)} className="hover:opacity-70 transition-opacity">
          {collapsed
            ? <ChevronRight className="inline w-3 h-3 text-[var(--text-muted)]" />
            : <ChevronDown className="inline w-3 h-3 text-[var(--text-muted)]" />
          }
        </button>
        <span className="text-[var(--text-muted)]">[</span>
        {collapsed ? (
          <span className="text-[var(--text-muted)] text-xs cursor-pointer" onClick={() => setCollapsed(false)}>
            {' '}{value.length} items{' '}
          </span>
        ) : (
          <div style={{ paddingLeft: '1.2rem' }}>
            {value.map((item, i) => (
              <div key={i}>
                <JsonNode value={item} depth={depth + 1} />
                {i < value.length - 1 && <span className="text-[var(--text-muted)]">,</span>}
              </div>
            ))}
          </div>
        )}
        <span className="text-[var(--text-muted)]">]</span>
      </span>
    );
  }

  if (typeof value === 'object') {
    const entries = Object.entries(value as Record<string, unknown>);
    if (entries.length === 0) return <span className="text-[var(--text-muted)]">{'{}'}</span>;
    return (
      <span>
        <button onClick={() => setCollapsed(!collapsed)} className="hover:opacity-70 transition-opacity">
          {collapsed
            ? <ChevronRight className="inline w-3 h-3 text-[var(--text-muted)]" />
            : <ChevronDown className="inline w-3 h-3 text-[var(--text-muted)]" />
          }
        </button>
        <span className="text-[var(--text-muted)">{'{'}</span>
        {collapsed ? (
          <span className="text-[var(--text-muted)] text-xs cursor-pointer" onClick={() => setCollapsed(false)}>
            {' '}{entries.length} keys{' '}
          </span>
        ) : (
          <div style={{ paddingLeft: '1.2rem' }}>
            {entries.map(([k, v], i) => (
              <div key={k}>
                <span className="text-purple-400">&quot;{k}&quot;</span>
                <span className="text-[var(--text-muted)]">: </span>
                <JsonNode value={v} depth={depth + 1} />
                {i < entries.length - 1 && <span className="text-[var(--text-muted)]">,</span>}
              </div>
            ))}
          </div>
        )}
        <span className="text-[var(--text-muted)]">{'}'}</span>
      </span>
    );
  }

  return <span>{String(value)}</span>;
}

export function JsonViewer({ data, title = 'Raw JSON Output' }: JsonViewerProps) {
  const [copied, setCopied] = useState(false);
  const [raw, setRaw] = useState(false);

  function handleCopy() {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="card animate-fade-in">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-[var(--text)]">{title}</h2>
        <div className="flex gap-2">
          <button
            onClick={() => setRaw(!raw)}
            className="text-xs px-2 py-1 rounded bg-[var(--surface-hover)] text-[var(--text-muted)] hover:text-[var(--text)] transition-colors"
          >
            {raw ? 'Tree' : 'Raw'}
          </button>
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 text-xs px-2 py-1 rounded bg-[var(--surface-hover)] text-[var(--text-muted)] hover:text-[var(--text)] transition-colors"
          >
            {copied ? <Check className="w-3 h-3 text-bullish" /> : <Copy className="w-3 h-3" />}
            {copied ? 'Copied!' : 'Copy'}
          </button>
        </div>
      </div>

      <div className="bg-surface rounded-lg p-3 overflow-auto max-h-96 scrollbar-thin">
        {raw ? (
          <pre className="text-xs font-mono text-[var(--text)] whitespace-pre-wrap">
            {JSON.stringify(data, null, 2)}
          </pre>
        ) : (
          <div className="text-xs font-mono text-[var(--text)] leading-relaxed">
            <JsonNode value={data} depth={0} />
          </div>
        )}
      </div>
    </div>
  );
}
