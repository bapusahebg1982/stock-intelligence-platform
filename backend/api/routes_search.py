from fastapi import APIRouter
import yfinance as yf
import difflib

router = APIRouter()

# 🔥 Expanded base universe (important for India)
STOCK_DB = [
    {"name": "Apple", "ticker": "AAPL"},
    {"name": "Microsoft", "ticker": "MSFT"},
    {"name": "Tesla", "ticker": "TSLA"},
    {"name": "Infosys", "ticker": "INFY.NS"},
    {"name": "Reliance Industries", "ticker": "RELIANCE.NS"},
    {"name": "TCS", "ticker": "TCS.NS"},
    {"name": "HDFC Bank", "ticker": "HDFCBANK.NS"},
    {"name": "Canara Bank", "ticker": "CANBK.NS"},
    {"name": "ICICI Bank", "ticker": "ICICIBANK.NS"},
    {"name": "State Bank of India", "ticker": "SBIN.NS"},
    {"name": "Delta Corp", "ticker": "DELTACORP.NS"},
]


def fuzzy_match(query, choices, key="name"):
    names = [c[key] for c in choices]
    matches = difflib.get_close_matches(query, names, n=5, cutoff=0.3)

    return [
        c for c in choices if c[key] in matches
    ]


@router.get("/search")
def search(q: str):

    q_lower = q.lower()

    results = []

    # 🔹 STEP 1: direct partial match
    for stock in STOCK_DB:
        if q_lower in stock["name"].lower() or q_lower in stock["ticker"].lower():
            results.append(stock)

    if results:
        return {"results": results[:10]}

    # 🔹 STEP 2: fuzzy match (handles “canara bank”, “infosyss” etc.)
    fuzzy = fuzzy_match(q_lower, STOCK_DB)

    if fuzzy:
        return {"results": fuzzy}

    # 🔹 STEP 3: try Yahoo Finance (ticker guess)
    try:
        guess = q.upper().replace(" ", "")

        for suffix in ["", ".NS"]:
            ticker = guess + suffix

            stock = yf.Ticker(ticker)
            info = stock.info

            name = info.get("longName") or info.get("shortName")

            if name:
                return {
                    "results": [
                        {"name": name, "ticker": ticker}
                    ]
                }

    except:
        pass

    return {"results": []}
