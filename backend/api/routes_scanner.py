from fastapi import APIRouter
from scanners.beaten_down import scan_market

router = APIRouter()

@router.get("/scan/beaten-down")
def beaten_down(market: str = "US", price_cap: float = None):

    try:
        results = scan_market(market, price_cap)

        return {
            "market": market,
            "count": len(results),
            "results": results
        }

    except Exception as e:
        return {
            "error": str(e),
            "market": market,
            "results": []
        }
