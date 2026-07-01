from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.config import get_settings, Settings
from app.services.mock_data import (
    get_mock_fundamentals, get_mock_technicals, get_mock_risk, TICKERS
)
from app.services.real_data import RealDataAdapter
from app.services.cache import CacheService
from app.scoring.engine import ZenRatingEngine
from functools import lru_cache

router = APIRouter()
engine = ZenRatingEngine()


@lru_cache()
def get_cache(settings: Settings = Depends(get_settings)) -> CacheService:
    return CacheService(settings.redis_url, settings.redis_ttl_seconds)


@router.get("/{ticker}", summary="Get Zen Rating composite score for a ticker")
async def get_score(
    ticker: str,
    settings: Settings = Depends(get_settings),
):
    ticker = ticker.upper().strip()
    if not ticker.isalpha() or len(ticker) > 10:
        raise HTTPException(status_code=400, detail="Invalid ticker symbol")

    cache = CacheService(settings.redis_url, settings.redis_ttl_seconds)
    cache_key = f"score:{ticker}:{settings.data_source}"
    cached = cache.get(cache_key)
    if cached:
        return {**cached, "cache_hit": True}

    if settings.data_source == "real":
        adapter = RealDataAdapter(settings)
        fundamentals = adapter.get_fundamentals(ticker)
        technicals = adapter.get_technicals(ticker)
        risk_data = adapter.get_risk(ticker)

        if not fundamentals:
            fundamentals = get_mock_fundamentals(ticker)
        if not technicals:
            technicals = get_mock_technicals(ticker)
        if not risk_data:
            risk_data = get_mock_risk(ticker)
        data_source = "real+mock_fallback"
    else:
        fundamentals = get_mock_fundamentals(ticker)
        technicals = get_mock_technicals(ticker)
        risk_data = get_mock_risk(ticker)
        data_source = "mock"

    result = engine.score(
        ticker=ticker,
        company_name=fundamentals.get("company_name", ticker),
        sector=fundamentals.get("sector", "Unknown"),
        industry=fundamentals.get("industry", "Unknown"),
        fundamentals=fundamentals,
        technicals=technicals,
        risk_data=risk_data,
        data_source=data_source,
    )

    cache.set(cache_key, result)
    return {**result, "cache_hit": False}


@router.get("/", summary="Screen multiple tickers at once")
async def screen_tickers(
    tickers: str = Query(..., description="Comma-separated tickers, e.g. AAPL,MSFT,GOOGL"),
    settings: Settings = Depends(get_settings),
):
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()][:20]
    if not ticker_list:
        raise HTTPException(status_code=400, detail="At least one ticker required")

    results = []
    for ticker in ticker_list:
        if not ticker.isalpha() or len(ticker) > 10:
            continue
        fundamentals = get_mock_fundamentals(ticker)
        technicals = get_mock_technicals(ticker)
        risk_data = get_mock_risk(ticker)
        result = engine.score(
            ticker=ticker,
            company_name=fundamentals.get("company_name", ticker),
            sector=fundamentals.get("sector", "Unknown"),
            industry=fundamentals.get("industry", "Unknown"),
            fundamentals=fundamentals,
            technicals=technicals,
            risk_data=risk_data,
            data_source="mock",
        )
        results.append(result)

    results.sort(key=lambda x: x["composite"]["total"], reverse=True)
    return {"count": len(results), "results": results}


@router.get("/watchlist/defaults", summary="Get scores for default watchlist")
async def get_default_watchlist(settings: Settings = Depends(get_settings)):
    tickers = list(TICKERS.keys())
    results = []
    for ticker in tickers:
        fundamentals = get_mock_fundamentals(ticker)
        technicals = get_mock_technicals(ticker)
        risk_data = get_mock_risk(ticker)
        result = engine.score(
            ticker=ticker,
            company_name=fundamentals.get("company_name", ticker),
            sector=fundamentals.get("sector", "Unknown"),
            industry=fundamentals.get("industry", "Unknown"),
            fundamentals=fundamentals,
            technicals=technicals,
            risk_data=risk_data,
            data_source="mock",
        )
        results.append({
            "ticker": ticker,
            "company_name": result["company_name"],
            "sector": result["sector"],
            "composite_score": result["composite"]["total"],
            "grade": result["composite"]["grade"],
            "trend": result["composite"]["trend"],
        })

    results.sort(key=lambda x: x["composite_score"], reverse=True)
    return {"count": len(results), "results": results}
