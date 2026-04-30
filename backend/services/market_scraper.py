import requests
from bs4 import BeautifulSoup


def scrape_sp500():

    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # 🔥 Try primary method
        table = soup.find("table", {"id": "constituents"})

        if table:
            return extract_tickers_from_table(table)

        # 🔥 Fallback: find ANY wikitable
        tables = soup.find_all("table", {"class": "wikitable"})

        for t in tables:
            tickers = extract_tickers_from_table(t)
            if tickers:
                return tickers

        return []

    except Exception as e:
        print("SP500 scrape failed:", e)
        return []


def scrape_nifty500():

    url = "https://en.wikipedia.org/wiki/NIFTY_500"

    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        tables = soup.find_all("table")

        tickers = []

        for table in tables:
            tickers += extract_tickers_from_table(table, suffix=".NS")

        return tickers

    except Exception as e:
        print("NIFTY scrape failed:", e)
        return []


def extract_tickers_from_table(table, suffix=""):

    tickers = []

    try:
        rows = table.find_all("tr")[1:]

        for row in rows:
            cols = row.find_all("td")

            if cols:
                ticker = cols[0].text.strip()

                # basic cleaning
                ticker = ticker.replace("\n", "").replace(".", "-")

                if ticker:
                    tickers.append(ticker + suffix)

    except:
        pass

    return tickers
