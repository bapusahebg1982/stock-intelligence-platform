import yfinance as yf
from utils.indicators import rsi
from core.gpt_analyst import generate_ai_analysis


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

        pe = info.get("trailingPE")
        growth = info.get("revenueGrowth")

        # scoring
        score = 50

        if rsi_val < 35:
            score += 15
        if price > ma50:
            score += 10
        if growth and growth > 0:
            score += 10
        if pe and pe < 30:
            score += 10

        base_data = {
            "ticker": ticker,
            "price": round(price, 2),
            "sector": info.get("sector", "Unknown"),

            "technicals": {
                "rsi": round(rsi_val, 2),
                "ma50": round(ma50, 2),
                "trend": "Bullish" if price > ma50 else "Bearish"
            },

            "fundamentals": {
                "pe": pe,
                "revenue_growth": growth
            },

            "high_low": {
                "1y_high": high,
                "1y_low": low
            },

            "score": score
        }

        # 🔥 AI ANALYSIS
        ai = generate_ai_analysis(base_data)

        base_data["ai_analysis"] = ai

        return base_data

    except Exception as e:
        return {"error": str(e)}
