from core.stock_analyzer import analyze_stock
from services.universe_service import get_universe


def scan_market(market="US", price_cap=None):

    universe = get_universe(market, limit=50)

    results = []

    for ticker in universe:

        try:
            stock = analyze_stock(ticker)

            if not stock:
                continue

            price = stock["price"]
            high = stock["high_low"]["1y_high"]

            if not price or not high:
                continue

            if price_cap and price > price_cap:
                continue

            drop = price / high

            if drop < 0.75 and stock["score"] >= 60:

                results.append({
                    "ticker": ticker,
                    "price": price,
                    "drop_pct": round((1 - drop) * 100, 2),
                    "sector": stock["sector"],
                    "score": stock["score"],
                    "reason": build_reason(stock)
                })

        except:
            continue

    return sorted(results, key=lambda x: x["score"], reverse=True)


def build_reason(stock):

    reasons = []

    if stock["technicals"]["rsi"] < 35:
        reasons.append("Oversold")

    if stock["technicals"]["trend"] == "Bearish":
        reasons.append("Below MA50")

    if stock["fundamentals"]["revenue_growth"]:
        reasons.append("Growth intact")

    return reasons
