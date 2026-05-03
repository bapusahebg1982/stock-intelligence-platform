from fastapi import APIRouter
from core.ticker_resolver import search_suggestions

router = APIRouter()

@router.get("/search")
def search(q: str):
    return {
        "results": search_suggestions(q)
    }
