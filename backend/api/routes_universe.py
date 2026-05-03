from fastapi import APIRouter
from universe.builder import build_universe

router = APIRouter()


@router.get("/build-universe")
def build():
    data = build_universe()
    return {
        "status": "ok",
        "us_count": len(data["US"]),
        "india_count": len(data["INDIA"])
    }
