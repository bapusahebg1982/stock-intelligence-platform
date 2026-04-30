from fastapi import APIRouter, Query

from scanners.beaten_down import scan_market
from core.universe_cache import get_universe

router = APIRouter()


@router.get("/beaten-down")
def beaten_down(
    market: str = "US",
    max_price: float = None
):

    universe = get_universe()

    tickers = universe.get(market.upper(), [])

    data = scan_market(
        universe=tickers,
        max_price=max_price,
        market=market
    )

    return {
        "market": market,
        "count": len(data),
        "results": data
    }
