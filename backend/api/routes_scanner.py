from fastapi import APIRouter
from scanners.beaten_down import scan_market

router = APIRouter()

@router.get("/scan/beaten-down")
def beaten_down(market: str = "US", price_cap: float = None):
    return {
        "market": market,
        "results": scan_market(market, price_cap)
    }