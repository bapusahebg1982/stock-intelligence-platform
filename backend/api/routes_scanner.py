from fastapi import APIRouter
from scanners.beaten_down import scan_market

router = APIRouter()

@router.get("/beaten-down")
def beaten_down(market: str = "US", max_price: float = None):

    data = scan_market(market, max_price)

    return {
        "market": market,
        "results": data
    }
