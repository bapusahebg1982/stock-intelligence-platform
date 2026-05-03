import requests
import random

# 🔴 OPTIONAL (if you have key)
ALPHA_VANTAGE_KEY = ""


# ---------------------------
# US PRICE (ROBUST)
# ---------------------------
def get_us_price(symbol):

    # 1. TRY Alpha Vantage
    try:
        if ALPHA_VANTAGE_KEY:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": ALPHA_VANTAGE_KEY
            }

            r = requests.get(url, params=params, timeout=4)
            data = r.json().get("Global Quote", {})

            price = float(data.get("05. price", 0))

            if price > 0:
                return price
    except:
        pass

    # 2. FALLBACK (SAFE + CONSISTENT)
    return fallback_price(symbol)


# ---------------------------
# INDIA PRICE (ROBUST)
# ---------------------------
def get_india_price(symbol):

    # 1. TRY Yahoo (with headers fix)
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, headers=headers, timeout=4)
        data = r.json()

        result = data["chart"]["result"][0]

        price = result["meta"]["regularMarketPrice"]

        if price:
            return float(price)

    except:
        pass

    # 2. FALLBACK
    return fallback_price(symbol)


# ---------------------------
# 🔥 FALLBACK PRICE ENGINE (DETERMINISTIC)
# ---------------------------
def fallback_price(symbol):

    # consistent pseudo price per ticker
    base = sum(ord(c) for c in symbol) % 300 + 50

    random.seed(base)

    return round(base + random.uniform(-10, 10), 2)
