from fastapi import APIRouter, Depends, HTTPException
from app.core.config import get_settings, Settings
from app.services.mock_data import get_mock_fundamentals
from app.services.real_data import RealDataAdapter

router = APIRouter()


@router.get("/{ticker}", summary="Get fundamental data for a ticker")
async def get_fundamentals(ticker: str, settings: Settings = Depends(get_settings)):
    ticker = ticker.upper().strip()
    if not ticker.isalpha() or len(ticker) > 10:
        raise HTTPException(status_code=400, detail="Invalid ticker symbol")

    if settings.data_source == "real":
        adapter = RealDataAdapter(settings)
        data = adapter.get_fundamentals(ticker)
        if data:
            return data

    return get_mock_fundamentals(ticker)
