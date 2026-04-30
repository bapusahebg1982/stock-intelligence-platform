from core.stock_analyzer import analyze_stock
from services.universe_service import get_universe


def get_sector_opportunities(ticker, market="US"):

    base = analyze_stock(ticker)

    if not base:
        return {"error": "Invalid ticker"}

    sector = base["sector"]

    universe = get_universe(market, limit=100)

    peers = []

    for t in universe:

        try:
            stock = analyze_stock(t)

            if not stock:
                continue

            # 🔥 SAME SECTOR ONLY
            if stock["sector"] != sector:
                continue

            peers.append(stock)

        except:
            continue

    if not peers:
        return {
            "ticker": ticker,
            "sector": sector,
            "better": [],
            "similar": []
        }

    # 🔥 RANK BY SCORE
    peers_sorted = sorted(peers, key=lambda x: x["score"], reverse=True)

    better = []
    similar = []

    for stock in peers_sorted:

        if stock["ticker"] == ticker:
            continue

        if stock["score"] > base["score"]:
            better.append(format_output(stock, "Better fundamentals/technicals"))

        elif abs(stock["score"] - base["score"]) <= 5:
            similar.append(format_output(stock, "Similar strength"))

    return {
        "ticker": ticker,
        "sector": sector,
        "base_score": base["score"],
        "better": better[:5],
        "similar": similar[:5]
    }


def format_output(stock, reason):

    return {
        "ticker": stock["ticker"],
        "price": stock["price"],
        "score": stock["score"],
        "sector": stock["sector"],
        "reason": build_reason(stock, reason)
    }


def build_reason(stock, base_reason):

    reasons = [base_reason]

    if stock["technicals"]["rsi"] < 35:
        reasons.append("Oversold")

    if stock["technicals"]["trend"] == "Bullish":
        reasons.append("Above MA50 (strong trend)")

    if stock["fundamentals"]["revenue_growth"]:
        reasons.append("Revenue growth positive")

    return reasons
