import yfinance as yf

# 🔥 minimal smart mapping (expand later via DB)
COMMON_MAPPINGS = {
    "RELIANCE": "RELIANCE.NS",
    "INFOSYS": "INFY.NS",
    "TCS": "TCS.NS",
    "HDFC": "HDFCBANK.NS",
    "ICICI": "ICICIBANK.NS",
    "APPLE": "AAPL",
    "GOOGLE": "GOOGL",
    "MICROSOFT": "MSFT"
}


def resolve_ticker(query: str):

    q = query.upper().strip()

    # 1. direct mapping
    if q in COMMON_MAPPINGS:
        return COMMON_MAPPINGS[q]

    # 2. try as-is (US ticker)
    try:
        stock = yf.Ticker(q)
        if stock.info.get("currentPrice"):
            return q
    except:
        pass

    # 3. try India (.NS)
    try:
        stock = yf.Ticker(q + ".NS")
        if stock.info.get("currentPrice"):
            return q + ".NS"
    except:
        pass

    return None


# 🔍 autocomplete suggestions
def search_suggestions(query: str):

    q = query.upper()

    results = []

    for name, ticker in COMMON_MAPPINGS.items():
        if q in name:
            results.append({
                "name": name.title(),
                "ticker": ticker
            })

    return results[:5]
