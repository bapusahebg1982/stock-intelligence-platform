import yfinance as yf


def calculate_drawdown(high, price):

    if not high or not price:
        return 0

    return ((high - price) / high) * 100


def is_beaten_down(stock_data):

    price = stock_data["price"]
    high = stock_data["high_52w"]
    pe = stock_data["pe"]

    drawdown = calculate_drawdown(high, price)

    score = 0

    # 🔥 core logic
    if drawdown > 30:
        score += 40

    if pe and pe < 20:
        score += 20

    if stock_data.get("growth") and stock_data["growth"] > 0:
        score += 20

    if stock_data.get("roe") and stock_data["roe"] > 10:
        score += 20

    return {
        "is_beaten_down": score >= 60,
        "score": score,
        "drawdown_pct": round(drawdown, 2)
    }


def scan_beaten_down(universe, market, max_price=None):

    results = []

    for t in universe:

        stock = yf.Ticker(t)
        info = stock.info or {}

        price = info.get("currentPrice")
        high = info.get("fiftyTwoWeekHigh")

        data = {
            "ticker": t,
            "price": price,
            "high_52w": high,
            "pe": info.get("trailingPE"),
            "growth": info.get("revenueGrowth"),
            "roe": info.get("returnOnEquity"),
            "market": market
        }

        beat = is_beaten_down(data)

        if beat["is_beaten_down"]:

            if max_price and price and price > max_price:
                continue

            results.append({
                **data,
                **beat
            })

    return sorted(results, key=lambda x: x["score"], reverse=True)
