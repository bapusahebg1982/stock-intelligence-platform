from fastapi import APIRouter, Query

from core.sector_engine import get_sector_opportunities

router = APIRouter()


# ----------------------------
# SECTOR OPPORTUNITIES API
# ----------------------------
@router.get("/sector-opportunities")
def sector_opportunities(
    ticker: str,
):

    universe = [
        "AAPL", "MSFT", "GOOGL", "META", "AMZN",
        "NVDA", "TSLA",
        "IBM", "ORCL", "INTC",
        "INFY.NS", "TCS.NS", "RELIANCE.NS"
    ]

    data = get_sector_opportunities(
        universe=universe,
        base_ticker=ticker
    )

    return {
        "base_ticker": ticker,
        "count": len(data),
        "results": data
    }
