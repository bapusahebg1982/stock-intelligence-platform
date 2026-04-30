from core.stock_analyzer import analyze_stock
from data.universe_us import US_UNIVERSE
from data.universe_in import INDIA_UNIVERSE

def scan_market(market="US", price_cap=None):

    universe = US_UNIVERSE if market == "US" else INDIA_UNIVERSE
    results = []

    for ticker in universe:

        stock = analyze_stock(ticker)

        if not stock or "error" in stock:
            continue

        price = stock["price"]
        high = stock["high_low"]["1y_high"]

        if not high:
            continue

        if price_cap and price > price_cap:
            continue

        drop = price / high

        if drop < 0.7:

            results.append({
                "ticker": ticker,
                "price": price,
                "drop_pct": round((1 - drop) * 100, 2),
                "sector": stock["sector"],
                "reason": [
                    "Trading significantly below 1Y high",
                    "Potential value zone",
                    "Watch for reversal confirmation"
                ]
            })

    return sorted(results, key=lambda x: x["drop_pct"], reverse=True)
