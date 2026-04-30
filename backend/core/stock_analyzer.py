import yfinance as yf

from utils.indicators import rsi
from core.consensus_engine import run_multi_ai

# ✅ SAFE IMPORT (cache layer)
try:
    from core.ai_cache import get_cache, set_cache
    CACHE_ENABLED = True
except Exception:
    CACHE_ENABLED = False


def analyze_stock(ticker):

    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1y")

        if df is None or df.empty:
            return {"error": "No data found for ticker"}

        # ---------------------------
        # PRICE DATA
        # ---------------------------
        price = float(df["Close"].iloc[-1])
        high = float(df["High"].max())
        low = float(df["Low"].min())

        # ---------------------------
        # TECHNICALS
        # ---------------------------
        rsi_val = float(rsi(df).iloc[-1])
        ma50 = float(df["Close"].rolling(50).mean().iloc[-1])

        # ---------------------------
        # FUNDAMENTALS
        # ---------------------------
        info = stock.info or {}

        pe = info.get("trailingPE")
        growth = info.get("revenueGrowth")
        sector = info.get("sector", "Unknown")

        # ---------------------------
        # SCORE ENGINE
        # ---------------------------
        score = 50

        if rsi_val < 35:
            score += 15
        elif rsi_val > 70:
            score -= 10

        if price > ma50:
            score += 10
        else:
            score -= 5

        if growth and growth > 0:
            score += 10

        if pe and pe < 25:
            score += 10

        score = max(0, min(100, score))

        # ---------------------------
        # BASE DATA STRUCTURE
        # ---------------------------
        base_data = {
            "ticker": ticker,
            "price": round(price, 2),
            "sector": sector,

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
                "1y_high": round(high, 2),
                "1y_low": round(low, 2)
            },

            "score": score
        }

        # ---------------------------
        # 🧠 AI + CACHE LAYER (SAFE)
        # ---------------------------
        cache_key = f"ai:{ticker}"

        try:
            if CACHE_ENABLED:
                cached = get_cache(cache_key)

                if cached:
                    base_data["ai_analysis"] = cached
                    base_data["cached"] = True
                else:
                    ai_result = run_multi_ai(base_data)
                    base_data["ai_analysis"] = ai_result
                    base_data["cached"] = False
                    set_cache(cache_key, ai_result)
            else:
                # fallback if cache module missing
                base_data["ai_analysis"] = run_multi_ai(base_data)
                base_data["cached"] = False

        except Exception as e:
            base_data["ai_analysis"] = {
                "error": f"AI layer failed: {str(e)}"
            }
            base_data["cached"] = False

        return base_data

    except Exception as e:
        return {
            "error": f"Stock analysis failed: {str(e)}"
        }
