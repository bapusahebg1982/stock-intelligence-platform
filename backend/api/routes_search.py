from fastapi import APIRouter
import yfinance as yf

router = APIRouter()

# optional base DB (fast hits)
STOCK_DB = [
    {"name": "Apple", "ticker": "AAPL"},
    {"name": "Microsoft", "ticker": "MSFT"},
    {"name": "Tesla", "ticker": "TSLA"},
    {"name": "Infosys", "ticker": "INFY.NS"},
    {"name": "Reliance Industries", "ticker": "RELIANCE.NS"},
    {"name": "Jain Irrigation Systems", "ticker": "JISLJALEQS.NS"},
    {"name": "Delta Corp", "ticker": "DELTACORP.NS"},
]


@router.get("/search")
def search(q: str):

    q = q.lower()
    results = []

    # 🔹 STEP 1: local DB search
    for stock in STOCK_DB:
        if q in stock["name"].lower() or q in stock["ticker"].lower():
            results.append(stock)

    # 🔹 STEP 2: if found → return
    if results:
        return {"results": results[:10]}

    # 🔹 STEP 3: fallback → Yahoo Finance lookup
    try:
        ticker = q.upper().replace(" ", "")

        stock = yf.Ticker(ticker)
        info = stock.info

        name = info.get("longName") or info.get("shortName")

        if name:
            return {
                "results": [
                    {
                        "name": name,
                        "ticker": ticker
                    }
                ]
            }

    except:
        pass

    # 🔹 STEP 4: try NSE format
    try:
        ticker = q.upper().replace(" ", "") + ".NS"

        stock = yf.Ticker(ticker)
        info = stock.info

        name = info.get("longName") or info.get("shortName")

        if name:
            return {
                "results": [
                    {
                        "name": name,
                        "ticker": ticker
                    }
                ]
            }

    except:
        pass

    return {"results": []}
