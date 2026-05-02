from fastapi import APIRouter
from core.news_engine import fetch_news

router = APIRouter()

@router.get("/news/{ticker}")
def get_news(ticker: str):
    try:
        news = fetch_news(ticker)
        return {"ticker": ticker, "news": news}
    except Exception as e:
        print("News error:", e)
        return {"ticker": ticker, "news": []}
