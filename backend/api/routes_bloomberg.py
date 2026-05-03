from fastapi import APIRouter

# 🔥 CRITICAL: USE PRODUCTION ENGINE
from scanners.production_engine import scan_market

router = APIRouter()


@router.get("/bloomberg/opportunities")
def opportunities(market: str = "US", max_price: float = None):

    try:
        data = scan_market(market, max_price)

        # 🚨 NEVER RETURN EMPTY
        if not data or len(data) == 0:
            return fallback()

        return {
            "market": market,
            "count": len(data),
            "results": data
        }

    except Exception as e:
        print("❌ SCAN ERROR:", str(e))
        return fallback()


# ---------------------------
# HARD FALLBACK (ONLY IF ENGINE FAILS)
# ---------------------------
def fallback():
    return {
        "market": "UNKNOWN",
        "count": 1,
        "results": [
            {
                "name": "ENGINE FAILURE",
                "ticker": "ERR",
                "price": 0,
                "drawdown_pct": 0,
                "volatility": 0,
                "score": 0,
                "reason_drop": ["Production engine not executing"],
                "reason_opportunity": ["Check backend route wiring"],
            }
        ]
    }
