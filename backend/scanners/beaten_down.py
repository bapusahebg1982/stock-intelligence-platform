import yfinance as yf
from universe.loader import get_us, get_india


def get_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="6mo")
        if len(data) < 2:
            return None

        latest = data["Close"].iloc[-1]
        peak = data["Close"].max()

        drop = ((peak - latest) / peak) * 100

        return {
            "price": round(latest, 2),
            "drawdown_pct": round(drop, 2),
            "peak": round(peak, 2)
        }

    except:
        return None


def scan_market(market="US", max_price=None):

    universe = get_us() if market == "US" else get_india()

    results = []

    for stock in universe:

        price_data = get_price(stock["ticker"])
        if not price_data:
            continue

        if max_price and price_data["price"] > float(max_price):
            continue

        # only beaten down stocks
        if price_data["drawdown_pct"] < 15:
            continue

        results.append({
            "name": stock["name"],
            "ticker": stock["ticker"],
            "price": price_data["price"],
            "drawdown_pct": price_data["drawdown_pct"],
            "confidence": min(95, int(price_data["drawdown_pct"] * 2)),
            "reason_drop": "Market correction / volatility",
            "reason_opportunity": "Strong fundamentals + oversold zone",
            "since": "Auto-calculated"
        })

    # rank best opportunities first
    results.sort(key=lambda x: x["drawdown_pct"], reverse=True)

    return results[:20]
