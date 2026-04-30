import yfinance as yf
from core.ai_engine import generate_stock_analysis


def analyze_stock(ticker):

    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}

        price = info.get("currentPrice")

        fundamentals = {
            "pe": info.get("trailingPE"),
            "revenue_growth": info.get("revenueGrowth")
        }

        technicals = {
            "rsi": None,
            "trend": "Unknown"
        }

        high_low = {
            "1y_high": info.get("fiftyTwoWeekHigh"),
            "1y_low": info.get("fiftyTwoWeekLow")
        }

        ai_analysis = generate_stock_analysis({
            "ticker": ticker,
            "price": price,
            "pe": fundamentals["pe"],
            "growth": fundamentals["revenue_growth"],
            "trend": technicals["trend"]
        })

        return {
            "ticker": ticker,
            "price": price,
            "fundamentals": fundamentals,
            "technicals": technicals,
            "high_low": high_low,
            "ai_analysis": ai_analysis,
            "score": 50
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "error": str(e)
        }
