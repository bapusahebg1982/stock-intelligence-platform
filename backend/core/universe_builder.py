import requests
from bs4 import BeautifulSoup


# ----------------------------
# FALLBACK (NEVER EMPTY)
# ----------------------------
FALLBACK_US = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    "NVDA", "TSLA", "NFLX", "IBM", "ORCL"
]

FALLBACK_INDIA = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS",
    "HDFCBANK.NS", "ICICIBANK.NS"
]


# ----------------------------
# S&P 500 SCRAPER
# ----------------------------
def get_sp500_tickers():

    try:
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            return FALLBACK_US

        soup = BeautifulSoup(res.text, "html.parser")

        table = soup.find("table", {"id": "constituents"})

        if not table:
            return FALLBACK_US

        tickers = []

        for row in table.find_all("tr")[1:]:

            cols = row.find_all("td")

            ticker = cols[0].text.strip()

            ticker = ticker.replace(".", "-")

            tickers.append(ticker)

        return tickers if tickers else FALLBACK_US

    except Exception:
        return FALLBACK_US


# ----------------------------
# INDIA (STATIC FOR NOW)
# ----------------------------
def get_india_tickers():
    return FALLBACK_INDIA


# ----------------------------
# MASTER BUILDER
# ----------------------------
def build_universe():

    us = get_sp500_tickers()
    india = get_india_tickers()

    return {
        "US": us if us else FALLBACK_US,
        "INDIA": india if india else FALLBACK_INDIA
    }
