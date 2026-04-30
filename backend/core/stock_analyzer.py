import yfinance as yf
from utils.indicators import rsi

def analyze_stock(ticker):

    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1y")

        if df.empty:
            return {"error": "Invalid ticker"}

        price = df["Close"].iloc[-1]
        high = df["High"].max()
        low = df["Low"].min()

        rsi_val = rsi(df).iloc[-1]
        ma50 = df["Close"].rolling(50).mean().iloc[-1]

        info = stock.info

        return {
            "ticker": ticker,
            "price": round(price, 2),
            "sector": info.get("sector", "Unknown"),

            "technicals": {
                "rsi": round(rsi_val, 2),
                "ma50": round(ma50, 2),
                "trend": "Bullish" if price > ma50 else "Bearish"
            },

            "fundamentals": {
                "pe": info.get("trailingPE"),
                "revenue_growth": info.get("revenueGrowth")
            },

            "high_low": {
                "1y_high": high,
                "1y_low": low
            }
        }

    except Exception as e:
        return {"error": str(e)}
