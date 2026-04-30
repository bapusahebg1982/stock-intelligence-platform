from core.stock_analyzer import analyze_stock
from services.market_universe import get_market_universe


def scan_market(market="US", price_cap=None):

    universe = get_market_universe(market)

    results = []

    for ticker in universe:

        stock = analyze_stock(ticker)

        if not stock:
            continue

        price = stock["price"]
        high = stock["high_low"]["1y_high"]

        if not high:
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

    return sorted(results, key=lambda x: x["score"], reverse=True)


def build_reason(stock):

    reasons = []

    if stock["technicals"]["rsi"] < 35:
        reasons.append("Oversold (RSI low)")

    if stock["technicals"]["trend"] == "Bearish":
        reasons.append("Below MA50 (reversal zone)")

    if stock["fundamentals"]["revenue_growth"]:
        reasons.append("Revenue still growing")

    if stock["score"] >= 70:
        reasons.append("Strong fundamentals despite drawdown")

    return reasons
