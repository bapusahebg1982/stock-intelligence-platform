import yfinance as yf
from core.ai_engine import generate_stock_analysis


def analyze_stock(ticker):

    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}

        price = info.get("currentPrice") or info.get("regularMarketPrice")

        if not price:
            return {
                "ticker": ticker,
                "error": "Invalid ticker or no price data"
            }

        ai_analysis = generate_stock_analysis({
            "ticker": ticker,
            "price": price
        })

        return {
            "ticker": ticker,
            "price": price,
            "ai_analysis": ai_analysis
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "error": str(e)
        }
