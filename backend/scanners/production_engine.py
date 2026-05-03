from core.data_provider import get_price_and_history
from core.feature_engine import compute_features
from core.ranking_engine import score_stock


US_UNIVERSE = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]
INDIA_UNIVERSE = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]


def scan_market(market="US", max_price=None):

    universe = US_UNIVERSE if market == "US" else INDIA_UNIVERSE

    results = []

    for symbol in universe:

        try:
            price, peak = get_price_and_history(symbol)

            if not price or not peak:
                continue

            features = compute_features(price, peak)

            if not features:
                continue

            score = score_stock(features)

            # FILTER
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
                    "Recent decline from 3-month highs",
                    "Short-term market pressure"
                ],

                "reason_opportunity": [
                    "Trading below recent peak",
                    "Potential mean reversion",
                    "Opportunity if fundamentals intact"
                ]
            })

        except Exception as e:
            print(f"❌ ERROR {symbol}: {e}")
            continue

    results.sort(key=lambda x: x["score"], reverse=True)

    return results
