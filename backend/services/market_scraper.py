import requests
from bs4 import BeautifulSoup


def scrape_sp500():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "html.parser")

    table = soup.find("table", {"id": "constituents"})

    tickers = []

    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        ticker = cols[0].text.strip()
        tickers.append(ticker)

    return tickers


def scrape_nifty500():

    # simplified (can expand later)
    url = "https://en.wikipedia.org/wiki/NIFTY_500"
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "html.parser")

    tables = soup.find_all("table")

    tickers = []

    for table in tables:
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            if cols:
                ticker = cols[0].text.strip()
                tickers.append(ticker + ".NS")

    return tickers
