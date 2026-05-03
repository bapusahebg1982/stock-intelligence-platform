from fastapi import APIRouter
from scanners.beaten_down import scan_market

router = APIRouter()

@router.get("/beaten-down")
def beaten_down(max_price: float = None):

    try:
        data = scan_market(max_price)
        return {"results": data}
    except Exception as e:
        return {"results": [], "error": str(e)}
