from core.data_provider import get_us_price, get_india_price
from core.feature_engine import compute_features
from core.ranking_engine import score_stock


US_UNIVERSE = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]
INDIA_UNIVERSE = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]


# simulate historical peak cache (replace with DB later)
PEAK_CACHE = {
    "AAPL": 220,
    "MSFT": 450,
    "TSLA": 300,
    "RELIANCE.NS": 3200,
    "TCS.NS": 4200
}


def scan_market(market="US", max_price=None):

    universe = US_UNIVERSE if market == "US" else INDIA_UNIVERSE

    results = []

    for symbol in universe:

        if market == "US":
            price = get_us_price(symbol)
        else:
            price = get_india_price(symbol)

        if not price:
            continue

        peak = PEAK_CACHE.get(symbol, price * 1.2)

        features = compute_features(price, peak)

        score = score_stock(features)

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
                "Strong long-term fundamentals"
            ]
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results
