import yfinance as yf

# 🔥 Expanded universe (still lightweight, but better coverage)
US_UNIVERSE = [
    "AAPL","MSFT","AMD","NVDA","TSLA","META",
    "F","INTC","PLTR","SOFI","NIO","LCID","RIVN"
]

INDIA_UNIVERSE = [
    "RELIANCE.NS","INFY.NS","TCS.NS","HDFCBANK.NS",
    "ITC.NS","SBIN.NS","TATAMOTORS.NS","ZOMATO.NS"
]


def analyze_stock(ticker):

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")

        if hist.empty:
            return None

        high = hist["High"].max()
        current = hist["Close"].iloc[-1]

        drawdown = ((current - high) / high) * 100

        # Only keep beaten-down
        if drawdown > -10:
            return None

        # 🔥 timeframe
        peak_date = hist["High"].idxmax()

        # 🔥 simple opportunity score
        score = abs(drawdown)

        return {
            "ticker": ticker,
            "price": round(current, 2),
            "drawdown_pct": round(drawdown, 2),
            "since": str(peak_date.date()),
            "score": round(score, 2)
        }

    except:
        return None


def scan_market(market="US", max_price=None):

    universe = US_UNIVERSE if market == "US" else INDIA_UNIVERSE

    results = []

    # 🔥 STEP 1: scan EVERYTHING
    for ticker in universe:
        data = analyze_stock(ticker)

        if data:
            results.append(data)

    # 🔥 STEP 2: rank FIRST (best opportunities)
    results.sort(key=lambda x: x["score"], reverse=True)

    # 🔥 STEP 3: apply filter AFTER ranking
    if max_price:
        results = [r for r in results if r["price"] <= max_price]

    # 🔥 STEP 4: if filter removes everything → fallback
    if not results:
        # return top opportunities anyway (no filter)
        results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:20]
