from fastapi import APIRouter
from core.stock_analyzer import analyze_stock

router = APIRouter()

@router.get("/analyze/{ticker}")
def analyze(ticker: str):

    result = analyze_stock(ticker)

    if not result:
        return {
            "ticker": ticker,
            "error": "No data returned"
        }

    return result
