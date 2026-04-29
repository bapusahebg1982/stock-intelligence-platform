from fastapi import APIRouter
from core.stock_analyzer import analyze_stock

router = APIRouter()

@router.get("/analyze/{ticker}")
def analyze(ticker: str):
    return analyze_stock(ticker)