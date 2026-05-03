import yfinance as yf
from core.intelligence_engine import generate_beaten_insight


US_UNIVERSE = ["AAPL", "MSFT", "AMD", "NVDA", "TSLA", "META"]
INDIA_UNIVERSE = ["RELIANCE.NS", "INFY.NS", "TCS.NS", "HDFCBANK.NS"]


def analyze_stock(ticker):

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")

        if hist.empty:
            return None

        high = hist["High"].max()
        current = hist["Close"].iloc[-1]

        drawdown = ((current - high) / high) * 100

        # 🔻 threshold
        if drawdown > -15:
            return None

        # 🕒 timeframe (approx)
        peak_date = hist["High"].idxmax()
        timeframe = str(peak_date.date())

        insight = generate_beaten_insight(
            ticker, round(current, 2), round(drawdown, 2), timeframe
        )

        return {
            "ticker": ticker,
            "price": round(current, 2),
            "drawdown_pct": round(drawdown, 2),
            "since": timeframe,
            "reason_drop": insight["reason_drop"],
            "reason_opportunity": insight["reason_opportunity"],
            "confidence": insight["confidence"]
        }

    except:
        return None


def scan_market(market="US", max_price=None):

    universe = US_UNIVERSE if market == "US" else INDIA_UNIVERSE

    results = []

    for ticker in universe:

        data = analyze_stock(ticker)

        if not data:
            continue

        if max_price and data["price"] > max_price:
            continue

        results.append(data)

    results.sort(key=lambda x: x["drawdown_pct"])

    return results
