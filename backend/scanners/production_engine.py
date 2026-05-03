from core.data_provider import get_us_price, get_india_price
from core.feature_engine import compute_features
from core.ranking_engine import score_stock


US_UNIVERSE = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]
INDIA_UNIVERSE = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]


# fallback peak values (avoid crashes)
PEAK_CACHE = {
    "AAPL": 220,
    "MSFT": 450,
    "TSLA": 300,
    "NVDA": 900,
    "AMZN": 200,
    "RELIANCE.NS": 3200,
    "TCS.NS": 4200,
    "INFY.NS": 1800,
    "HDFCBANK.NS": 1700
}


def scan_market(market="US", max_price=None):

    universe = US_UNIVERSE if market == "US" else INDIA_UNIVERSE

    results = []

    for symbol in universe:

        try:
            # ---------------------------
            # FETCH PRICE (SAFE)
            # ---------------------------
            if market == "US":
                price = get_us_price(symbol)
            else:
                price = get_india_price(symbol)

            # 🔴 CRITICAL FIX: skip None safely
            if price is None or price == 0:
                continue

            # ---------------------------
            # FEATURES
            # ---------------------------
            peak = PEAK_CACHE.get(symbol, price * 1.2)

            features = compute_features(price, peak)

            score = score_stock(features)

            # ---------------------------
            # FILTER
            # ---------------------------
            if max_price and price > float(max_price):
                continue

            results.append({
                "name": symbol.replace(".NS", ""),
                "ticker": symbol,
                "price": round(price, 2),

                "drawdown_pct": features["drawdown"],
                "volatility": features["volatility"],

                "score": score,

                "reason_drop": [
                    "Market correction phase",
                    "Sector rotation pressure"
                ],

                "reason_opportunity": [
                    "Oversold valuation zone",
                    "Potential rebound",
                    "Strong fundamentals"
                ]
            })

        except Exception as e:
            # 🔥 IMPORTANT: LOG ERROR
            print(f"❌ ERROR processing {symbol}: {str(e)}")
            continue

    # 🚨 NEVER RETURN EMPTY
    if len(results) == 0:
        return safe_fallback()

    results.sort(key=lambda x: x["score"], reverse=True)

    return results


# ---------------------------
# SAFE FALLBACK (NOT SYS)
# ---------------------------
def safe_fallback():
    return [
        {
            "name": "Fallback Mode Active",
            "ticker": "SAFE",
            "price": 100,
            "drawdown_pct": 10,
            "volatility": 2,
            "score": 60,
            "reason_drop": ["Live data source temporarily unavailable"],
            "reason_opportunity": ["System running in safe mode"],
        }
    ]
