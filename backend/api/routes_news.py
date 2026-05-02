from fastapi import APIRouter
from core.news_engine import fetch_news, analyze_news

router = APIRouter()


@router.get("/news/{ticker}")
def get_news(ticker: str):

    try:
        raw_news = fetch_news(ticker)
        analyzed = analyze_news(raw_news)

        return {
            "ticker": ticker,
            "news": analyzed
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "error": str(e),
            "news": []
        }
