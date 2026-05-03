from fastapi import APIRouter
from scanners.bloomberg_engine import run_bloomberg_scan

router = APIRouter()


@router.get("/bloomberg/opportunities")
def opportunities(market: str = "US", max_price: float = None):

    data = run_bloomberg_scan(market, max_price)

    return {
        "market": market,
        "count": len(data),
        "results": data
    }
