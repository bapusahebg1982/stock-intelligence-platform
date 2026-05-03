import requests


def get_price_and_history(symbol):

    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=3mo&interval=1d"

        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers, timeout=5)
        data = r.json()

        result = data["chart"]["result"][0]

        prices = result["indicators"]["quote"][0]["close"]

        prices = [p for p in prices if p]

        if not prices:
            return None, None

        current_price = prices[-1]
        peak_price = max(prices)

        return float(current_price), float(peak_price)

    except Exception as e:
        print(f"❌ DATA ERROR {symbol}: {e}")
        return None, None
