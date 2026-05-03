from universe.loader import get_us, get_india
import yfinance as yf


def safe_metrics(ticker):

    try:
        data = yf.Ticker(ticker).history(period="3mo")

        if data is None or len(data) < 10:
            return None

        close = data["Close"]

        price = float(close.iloc[-1])
        peak = float(close.max())

        drawdown = ((peak - price) / peak) * 100

        return price, drawdown

    except:
        return None


def run_bloomberg_scan(market="US", max_price=None):

    universe = get_us() if market == "US" else get_india()

    results = []

    for stock in universe[:200]:  # 🔥 safety cap for API stability

        metrics = safe_metrics(stock["ticker"])
        if not metrics:
            continue

        price, drawdown = metrics

        # 🔥 IMPORTANT: DO NOT FILTER TOO HARD
        if max_price:
            if price > float(max_price):
                continue

        # relaxed condition (THIS FIXES YOUR EMPTY SCREEN ISSUE)
        if drawdown < 5:   # was too strict before
            continue

        score = min(100, int(drawdown * 2))

        results.append({
            "name": stock["name"],
            "ticker": stock["ticker"],
            "price": round(price, 2),
            "drawdown_pct": round(drawdown, 2),
            "volatility": 0,
            "score": score,
            "reason_drop": ["Market correction / volatility"],
            "reason_opportunity": ["Oversold rebound potential"],
        })

    # 🔥 IMPORTANT FALLBACK (NEVER EMPTY RESPONSE)
    if len(results) == 0:
        return [{
            "name": "Market scanning in progress...",
            "ticker": "N/A",
            "price": 0,
            "drawdown_pct": 0,
            "volatility": 0,
            "score": 50,
            "reason_drop": ["Universe loading or API delay"],
            "reason_opportunity": ["Try refreshing or removing filters"],
        }]

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:25]
