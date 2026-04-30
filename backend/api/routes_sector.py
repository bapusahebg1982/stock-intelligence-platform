from fastapi import APIRouter

from core.sector_engine import get_sector_opportunities
from core.universe_cache import get_universe

router = APIRouter()


@router.get("/sector-opportunities")
def sector_opportunities(ticker: str):

    universe = get_universe()

    market = "INDIA" if ".NS" in ticker else "US"

    tickers = universe.get(market, [])

    data = get_sector_opportunities(
        universe=tickers,
        base_ticker=ticker
    )

    return {
        "ticker": ticker,
        "market": market,
        "count": len(data),
        "results": data[:10]  # top 10 only
    }
