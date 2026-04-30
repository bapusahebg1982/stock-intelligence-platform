import yfinance as yf


def calculate_drawdown(high, price):

    if not high or not price:
        return 0

    return ((high - price) / high) * 100


def is_beaten_down(price, high, pe, growth, roe):

    drawdown = calculate_drawdown(high, price)

    score = 0

    if drawdown > 30:
        score += 40

    if pe and pe < 20:
        score += 20

    if growth and growth > 0:
        score += 20

    if roe and roe > 10:
        score += 20

    return {
        "is_beaten_down": score >= 60,
        "score": score,
        "drawdown_pct": round(drawdown, 2)
    }


# ✅ THIS IS WHAT YOUR ROUTER EXPECTS
def scan_market(universe, max_price=None, market="US"):

    results = []

    for ticker in universe:

        try:
            stock = yf.Ticker(ticker)
            info = stock.info or {}

            price = info.get("currentPrice")
            high = info.get("fiftyTwoWeekHigh")

            if not price or not high:
                continue

            if max_price and price > max_price:
                continue

            result = is_beaten_down(
                price=price,
                high=high,
                pe=info.get("trailingPE"),
                growth=info.get("revenueGrowth"),
                roe=info.get("returnOnEquity")
            )

            if result["is_beaten_down"]:

                results.append({
                    "ticker": ticker,
                    "market": market,
                    "price": price,
                    "high_52w": high,
                    "pe": info.get("trailingPE"),
                    "growth": info.get("revenueGrowth"),
                    "roe": info.get("returnOnEquity"),
                    **result
                })

        except Exception:
            continue

    return sorted(results, key=lambda x: x["score"], reverse=True)
