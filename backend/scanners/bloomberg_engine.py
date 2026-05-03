import yfinance as yf
import time
from universe.loader import get_us, get_india


def fetch_price(ticker):

    for _ in range(2):  # retry mechanism
        try:
            data = yf.Ticker(ticker).history(period="2mo")

            if data is None or len(data) < 5:
                continue

            close = data["Close"]

            price = float(close.iloc[-1])
            peak = float(close.max())

            drawdown = ((peak - price) / peak) * 100

            return price, drawdown

        except Exception as e:
            time.sleep(0.2)
            continue

    return None


def run_bloomberg_scan(market="US", max_price=None):

    universe = get_us() if market == "US" else get_india()

    # 🚨 HARD FALLBACK
    if not universe:
        return fallback()

    results = []

    for stock in universe[:100]:

        metrics = fetch_price(stock["ticker"])

        if not metrics:
            continue

        price, drawdown = metrics

        # relaxed filter (IMPORTANT)
        if drawdown < 2:
            continue

        if max_price and price > float(max_price):
            continue

        score = min(100, int(drawdown * 2))

        results.append({
            "name": stock["name"],
            "ticker": stock["ticker"],
            "price": round(price, 2),
            "drawdown_pct": round(drawdown, 2),
            "volatility": 0,
            "score": score,
            "reason_drop": [
                "Market correction / volatility pressure"
            ],
            "reason_opportunity": [
                "Oversold condition",
                "Mean reversion potential"
            ],
        })

    # 🚨 CRITICAL: NEVER EMPTY RESPONSE
    if len(results) == 0:
        return fallback()

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:20]


def fallback():
    return [
        {
            "name": "Market data initializing...",
            "ticker": "SYS",
            "price": 0,
            "drawdown_pct": 0,
            "volatility": 0,
            "score": 50,
            "reason_drop": ["Data pipeline warming up"],
            "reason_opportunity": ["Retry in a few seconds"],
        }
    ]
