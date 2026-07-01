from fastapi import APIRouter, Depends, HTTPException
from app.core.config import get_settings, Settings
from app.services.mock_data import get_mock_risk
from app.services.real_data import RealDataAdapter

router = APIRouter()


@router.get("/{ticker}", summary="Get risk metrics for a ticker")
async def get_risk(ticker: str, settings: Settings = Depends(get_settings)):
    ticker = ticker.upper().strip()
    if not ticker.isalpha() or len(ticker) > 10:
        raise HTTPException(status_code=400, detail="Invalid ticker symbol")

    if settings.data_source == "real":
        adapter = RealDataAdapter(settings)
        data = adapter.get_risk(ticker)
        if data:
            return data

    return get_mock_risk(ticker)
