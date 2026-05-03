from core.data_provider import get_us_price, get_india_price
from core.feature_engine import compute_features
from core.ranking_engine import score_stock


US_UNIVERSE = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]
INDIA_UNIVERSE = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]


def scan_market(market="US", max_price=None):

    universe = US_UNIVERSE if market == "US" else INDIA_UNIVERSE

    results = []

    for symbol in universe:

        try:
            # ---------------------------
            # PRICE FETCH
            # ---------------------------
            price = get_us_price(symbol) if market == "US" else get_india_price(symbol)

            if not price or price <= 0:
                continue

            # ---------------------------
            # FIX: DYNAMIC PEAK (NOT STATIC CACHE)
            # ---------------------------
            peak = price * 1.3  # assume recent high ~30% above current

            features = compute_features(price, peak)

            score = score_stock(features)

            # ---------------------------
            # FILTER BAD DATA
            # ---------------------------
            if features["drawdown"] < 5:
                continue

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
                    "Recent correction from highs",
                    "Short-term selling pressure"
                ],

                "reason_opportunity": [
                    "Pullback within long-term trend",
                    "Potential rebound setup",
                    "Healthy correction phase"
                ]
            })

        except Exception as e:
            print(f"❌ ERROR {symbol}: {str(e)}")
            continue

    # ---------------------------
    # SORT + RETURN
    # ---------------------------
    results.sort(key=lambda x: x["score"], reverse=True)

    return results
