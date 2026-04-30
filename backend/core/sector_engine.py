import yfinance as yf


def safe_get_stock_data(ticker):

    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}

        return {
            "ticker": ticker,
            "sector": info.get("sector", "Unknown"),
            "market": "INDIA" if ".NS" in ticker else "US",
            "price": info.get("currentPrice"),
            "pe": info.get("trailingPE"),
            "growth": info.get("revenueGrowth"),
            "roe": info.get("returnOnEquity"),
        }

    except Exception:
        return None


def score_stock(stock, base_price):

    score = 50

    try:
        if stock["growth"] and stock["growth"] > 0:
            score += 10

        if stock["pe"] and stock["pe"] < 25:
            score += 10

        if stock["roe"] and stock["roe"] > 10:
            score += 10

        if stock["price"] and base_price and stock["price"] < base_price:
            score += 10

    except Exception:
        pass

    return score


def get_sector_opportunities(universe, base_ticker):

    base = safe_get_stock_data(base_ticker)

    if not base:
        return []

    results = []

    for ticker in universe:

        data = safe_get_stock_data(ticker)

        if not data:
            continue

        # ✅ SAME MARKET
        if data["market"] != base["market"]:
            continue

        # ✅ SAME SECTOR
        if data["sector"] != base["sector"]:
            continue

        data["score"] = score_stock(data, base["price"])

        results.append(data)

    return sorted(results, key=lambda x: x["score"], reverse=True)
