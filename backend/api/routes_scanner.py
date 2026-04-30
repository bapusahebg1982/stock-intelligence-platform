from fastapi import APIRouter, Query

from scanners.beaten_down import scan_market

router = APIRouter()


# ----------------------------
# BEATEN DOWN STOCKS API
# ----------------------------
@router.get("/beaten-down")
def beaten_down(
    max_price: float = None,
    market: str = "US"
):

    # ⚠️ TEMP UNIVERSAL LIST (replace later with scraper universe)
    universe = [
        "AAPL", "MSFT", "AMZN", "GOOGL", "META",
        "TSLA", "NFLX", "NVDA",
        "IBM", "INTC", "ORCL",
        "INFY.NS", "TCS.NS", "RELIANCE.NS"
    ]

    data = scan_market(
        universe=universe,
        max_price=max_price,
        market=market
    )

    return {
        "market": market,
        "max_price": max_price,
        "count": len(data),
        "results": data
    }
