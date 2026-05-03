import yfinance as yf
from core.intelligence_engine import generate_beaten_insight

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

        if drawdown > -10:
            return None

        peak_date = hist["High"].idxmax()

        insight = generate_beaten_insight(
            ticker,
            round(current, 2),
            round(drawdown, 2),
            str(peak_date.date())
        )

        score = abs(drawdown)

        return {
            "ticker": ticker,
            "price": round(current, 2),
            "drawdown_pct": round(drawdown, 2),
            "since": str(peak_date.date()),
            "reason_drop": insight.get("reason_drop"),
            "reason_opportunity": insight.get("reason_opportunity"),
            "confidence": insight.get("confidence"),
            "score": score
        }

    except Exception as e:
        print("Error:", ticker, e)
        return None


def scan_market(market="US", max_price=None):

    universe = US_UNIVERSE if market == "US" else INDIA_UNIVERSE

    results = []

    for ticker in universe:
        data = analyze_stock(ticker)
        if data:
            results.append(data)

    # rank first
    results.sort(key=lambda x: x["score"], reverse=True)

    # apply filter AFTER ranking
    if max_price:
        filtered = [r for r in results if r["price"] <= max_price]
        if filtered:
            results = filtered

    return results[:20]
