from fastapi import APIRouter
from core.stock_analyzer import analyze_stock
from core.ticker_resolver import resolve_ticker

router = APIRouter()

@router.get("/analyze/{query}")
def analyze(query: str):

    ticker = resolve_ticker(query)

    if not ticker:
        return {
            "error": "Ticker not found"
        }

    result = analyze_stock(ticker)
    result["resolved_ticker"] = ticker

    return result
