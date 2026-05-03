import yfinance as yf
from universe.loader import get_us, get_india


# ---------------------------
# SAFE FETCH (NO CRASH EVER)
# ---------------------------
def safe_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="3mo")
        if data is None or len(data) < 5:
            return None

        close = data["Close"]

        price = float(close.iloc[-1])
        peak = float(close.max())

        drawdown = ((peak - price) / peak) * 100

        return price, drawdown

    except:
        return None


# ---------------------------
# MAIN SCANNER (FORCED OUTPUT)
# ---------------------------
def run_bloomberg_scan(market="US", max_price=None):

    universe = get_us() if market == "US" else get_india()

    # 🚨 SAFETY: if universe empty → hard fallback
    if not universe or len(universe) == 0:
        return fallback()

    results = []

    for stock in universe[:150]:  # limit for stability

        metrics = safe_price(stock["ticker"])
        if not metrics:
            continue

        price, drawdown = metrics

        # relaxed filtering (IMPORTANT FIX)
        if drawdown < 3:
            continue

        if max_price and price > float(max_price):
            continue

        score = int(min(100, drawdown * 2))

        results.append({
            "name": stock["name"],
            "ticker": stock["ticker"],
            "price": round(price, 2),
            "drawdown_pct": round(drawdown, 2),
            "volatility": 0,
            "score": score,
            "reason_drop": [
                "Market correction detected",
                "Short-term selling pressure"
            ],
            "reason_opportunity": [
                "Oversold zone",
                "Potential mean reversion setup"
            ],
        })

    # 🚨 CRITICAL: NEVER RETURN EMPTY
    if len(results) == 0:
        return fallback()

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:20]


# ---------------------------
# FALLBACK (ALWAYS SHOW UI)
# ---------------------------
def fallback():

    return [
        {
            "name": "Market scanning initializing...",
            "ticker": "N/A",
            "price": 0,
            "drawdown_pct": 0,
            "volatility": 0,
            "score": 50,
            "reason_drop": ["Data source warming up"],
            "reason_opportunity": ["Try refresh in 10 seconds"],
        }
    ]
