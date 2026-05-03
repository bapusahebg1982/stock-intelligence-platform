from fastapi import APIRouter
from scanners.production_engine import scan_market

router = APIRouter()


@router.get("/bloomberg/opportunities")
def opportunities(market: str = "US", max_price: float = None):

    data = scan_market(market, max_price)

    return {
        "market": market,
        "count": len(data),
        "results": data
    }
