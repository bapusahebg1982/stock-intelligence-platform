import requests
from bs4 import BeautifulSoup


# ----------------------------
# S&P 500 (US MARKET)
# ----------------------------
def get_sp500_tickers():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    table = soup.find("table", {"id": "constituents"})

    tickers = []

    for row in table.find_all("tr")[1:]:

        cols = row.find_all("td")

        ticker = cols[0].text.strip()

        # Yahoo format fix
        ticker = ticker.replace(".", "-")

        tickers.append(ticker)

    return tickers


# ----------------------------
# INDIA (NIFTY 50)
# ----------------------------
def get_nifty50_tickers():

    # Static for now (stable + safe)
    tickers = [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS",
        "ICICIBANK.NS", "HINDUNILVR.NS", "SBIN.NS",
        "BAJFINANCE.NS", "KOTAKBANK.NS"
    ]

    return tickers


# ----------------------------
# MASTER UNIVERSE
# ----------------------------
def build_universe():

    try:
        us = get_sp500_tickers()
    except:
        us = []

    india = get_nifty50_tickers()

    return {
        "US": us,
        "INDIA": india
    }
