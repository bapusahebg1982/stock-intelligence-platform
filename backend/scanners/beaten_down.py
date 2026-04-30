import yfinance as yf
from core.ai_engine import generate_beaten_reason


def scan_market(universe):

    results = []

    for ticker in universe:

        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")

            if hist.empty:
                continue

            high = hist["Close"].max()
            current = hist["Close"].iloc[-1]

            drawdown = ((high - current) / high) * 100

            if drawdown < 20:
                continue

            data = {
                "ticker": ticker,
                "price": current,
                "drawdown_pct": round(drawdown, 2)
            }

            data["reason"] = generate_beaten_reason(data)

            results.append(data)

        except:
            continue

    return sorted(results, key=lambda x: x["drawdown_pct"], reverse=True)
