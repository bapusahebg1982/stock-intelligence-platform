from fastapi import APIRouter, Query
from scanners.bloomberg_engine import run_bloomberg_scan

router = APIRouter()


@router.get("/bloomberg/opportunities")
def opportunities(
    market: str = "US",
    max_price: float = None
):

    data = run_bloomberg_scan(market, max_price)

    # 🔥 CRITICAL FIX: ALWAYS RETURN SOMETHING
    if not data:
        return {
            "market": market,
            "count": 0,
            "results": [],
            "message": "No scan results - universe or price filter too strict"
        }

    return {
        "market": market,
        "count": len(data),
        "results": data
    }
