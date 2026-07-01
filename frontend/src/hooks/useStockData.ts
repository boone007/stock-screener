'use client';
import useSWR from 'swr';
import { fetchJson, V1 } from '@/utils/api';
import type {
  ZenRating, TechnicalData, FundamentalsData,
  SentimentData, RiskData, WatchlistItem
} from '@/types/stock';

const SWR_OPTIONS = {
  revalidateOnFocus: false,
  dedupingInterval: 30_000,
  errorRetryCount: 2,
};

export function useZenRating(ticker: string | null) {
  return useSWR<ZenRating>(
    ticker ? `${V1}/score/${ticker.toUpperCase()}` : null,
    (url: string) => fetchJson<ZenRating>(url),
    SWR_OPTIONS
  );
}

export function useTechnicals(ticker: string | null) {
  return useSWR<TechnicalData>(
    ticker ? `${V1}/technicals/${ticker.toUpperCase()}` : null,
    (url: string) => fetchJson<TechnicalData>(url),
    SWR_OPTIONS
  );
}

export function useFundamentals(ticker: string | null) {
  return useSWR<FundamentalsData>(
    ticker ? `${V1}/fundamentals/${ticker.toUpperCase()}` : null,
    (url: string) => fetchJson<FundamentalsData>(url),
    SWR_OPTIONS
  );
}

export function useSentiment(ticker: string | null) {
  return useSWR<SentimentData>(
    ticker ? `${V1}/sentiment/${ticker.toUpperCase()}` : null,
    (url: string) => fetchJson<SentimentData>(url),
    SWR_OPTIONS
  );
}

export function useRisk(ticker: string | null) {
  return useSWR<RiskData>(
    ticker ? `${V1}/risk/${ticker.toUpperCase()}` : null,
    (url: string) => fetchJson<RiskData>(url),
    SWR_OPTIONS
  );
}

export function useWatchlist() {
  return useSWR<{ count: number; results: WatchlistItem[] }>(
    `${V1}/score/watchlist/defaults`,
    (url: string) => fetchJson<{ count: number; results: WatchlistItem[] }>(url),
    { ...SWR_OPTIONS, revalidateOnMount: true }
  );
}
