from fastapi import APIRouter
from core.sector_engine import get_sector_opportunities

router = APIRouter()


@router.get("/sector/{ticker}")
def sector_analysis(ticker: str, market: str = "US"):

    try:
        result = get_sector_opportunities(ticker, market)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
