from fastapi import APIRouter
from scanners.beaten_down import scan_market
from services.universe_service import refresh_universe

router = APIRouter()


# 🔹 Beaten-down scanner
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


# 🔹 Refresh market universe (DB)
@router.get("/refresh-universe")
def refresh():

    try:
        data = refresh_universe()

        return {
            "status": "success",
            "data": data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
