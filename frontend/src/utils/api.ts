const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const V1 = `${API_BASE}/api/v1`;

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    next: { revalidate: 60 },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  score: (ticker: string) => fetchJson(`${V1}/score/${ticker}`),
  screenMultiple: (tickers: string[]) =>
    fetchJson(`${V1}/score/?tickers=${tickers.join(',')}`),
  watchlistDefaults: () => fetchJson(`${V1}/score/watchlist/defaults`),
  fundamentals: (ticker: string) => fetchJson(`${V1}/fundamentals/${ticker}`),
  technicals: (ticker: string) => fetchJson(`${V1}/technicals/${ticker}`),
  sentiment: (ticker: string) => fetchJson(`${V1}/sentiment/${ticker}`),
  risk: (ticker: string) => fetchJson(`${V1}/risk/${ticker}`),
};

export const fetcher = (url: string) => fetchJson(url);
export { V1, API_BASE };
