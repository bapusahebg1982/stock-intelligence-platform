import yfinance as yf

# 🔥 dynamic universe (expand later with DB)
US_UNIVERSE = ["AAPL", "MSFT", "AMD", "NVDA", "TSLA", "META"]
INDIA_UNIVERSE = ["RELIANCE.NS", "INFY.NS", "TCS.NS", "HDFCBANK.NS"]

UNIVERSE = US_UNIVERSE + INDIA_UNIVERSE


def get_drawdown(stock):

    try:
        hist = stock.history(period="1y")

        if hist.empty:
            return None

        high = hist["High"].max()
        current = hist["Close"].iloc[-1]

        drawdown = ((current - high) / high) * 100

        return current, round(drawdown, 2)

    except:
        return None


def scan_market(max_price=None):

    results = []

    for ticker in UNIVERSE:

        try:
            stock = yf.Ticker(ticker)

            data = get_drawdown(stock)

            if not data:
                continue

            price, drawdown = data

            # 🔻 only beaten-down
            if drawdown > -15:
                continue

            # 🎯 price filter
            if max_price and price > max_price:
                continue

            results.append({
                "ticker": ticker,
                "price": round(price, 2),
                "drawdown_pct": drawdown
            })

        except:
            continue

    # 🔥 sort most beaten-down first
    results.sort(key=lambda x: x["drawdown_pct"])

    return results[:20]
