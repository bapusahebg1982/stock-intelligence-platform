import yfinance as yf


# ----------------------------
# SINGLE STOCK DATA FETCH
# ----------------------------
def get_stock_data(ticker):

    stock = yf.Ticker(ticker)
    info = stock.info or {}

    return {
        "ticker": ticker,
        "sector": info.get("sector", "Unknown"),
        "market": "US" if ".NS" not in ticker else "INDIA",
        "price": info.get("currentPrice"),
        "pe": info.get("trailingPE"),
        "growth": info.get("revenueGrowth"),
        "roe": info.get("returnOnEquity"),
        "high_52w": info.get("fiftyTwoWeekHigh")
    }


# ----------------------------
# SECTOR PEER SCORING
# ----------------------------
def score_stock(stock, base_price):

    score = 50

    if stock["growth"] and stock["growth"] > 0:
        score += 10

    if stock["pe"] and stock["pe"] < 25:
        score += 10

    if stock["roe"] and stock["roe"] > 10:
        score += 10

    if stock["price"] and stock["price"] < base_price:
        score += 10

    return score


# ----------------------------
# MAIN FUNCTION (FIXED IMPORT)
# ----------------------------
def get_sector_opportunities(universe, base_ticker):

    base = get_stock_data(base_ticker)

    results = []

    for t in universe:

        data = get_stock_data(t)

        # 🚨 SAME MARKET FILTER (FIX YOUR EARLIER BUG)
        if data["market"] != base["market"]:
            continue

        # SAME SECTOR ONLY
        if data["sector"] != base["sector"]:
            continue

        data["score"] = score_stock(data, base["price"])

        results.append(data)

    return sorted(results, key=lambda x: x["score"], reverse=True)


# ----------------------------
# OPTIONAL BACKWARD COMPATIBILITY
# ----------------------------
def get_sector_data(ticker):
    return get_stock_data(ticker)
