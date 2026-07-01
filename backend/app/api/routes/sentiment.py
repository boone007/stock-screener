from fastapi import APIRouter, Depends, HTTPException
from app.core.config import get_settings, Settings
from app.services.mock_data import get_mock_sentiment

router = APIRouter()


@router.get("/{ticker}", summary="Get sentiment analysis for a ticker")
async def get_sentiment(ticker: str, settings: Settings = Depends(get_settings)):
    ticker = ticker.upper().strip()
    if not ticker.isalpha() or len(ticker) > 10:
        raise HTTPException(status_code=400, detail="Invalid ticker symbol")

    return get_mock_sentiment(ticker)
