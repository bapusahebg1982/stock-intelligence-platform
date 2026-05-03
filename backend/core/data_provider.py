import requests
import time

# ---------------------------
# REAL DATA PROVIDER (HYBRID)
# ---------------------------

ALPHA_VANTAGE_KEY = "YOUR_KEY_HERE"


# US STOCK DATA
def get_us_price(symbol):

    try:
        url = f"https://www.alphavantage.co/query"

        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_KEY
        }

        r = requests.get(url, params=params, timeout=5)
        data = r.json().get("Global Quote", {})

        price = float(data.get("05. price", 0))

        return price

    except:
        return None


# INDIA STOCK DATA (NSE UNOFFICIAL)
def get_india_price(symbol):

    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"

        r = requests.get(url, timeout=5)
        data = r.json()

        result = data["chart"]["result"][0]

        price = result["meta"]["regularMarketPrice"]

        return float(price)

    except:
        return None
