from fastapi import APIRouter

router = APIRouter()

# 🔥 Minimal database (expand later)
STOCK_DB = [
    {"name": "Apple", "ticker": "AAPL"},
    {"name": "Microsoft", "ticker": "MSFT"},
    {"name": "Tesla", "ticker": "TSLA"},
    {"name": "Infosys", "ticker": "INFY.NS"},
    {"name": "Reliance Industries", "ticker": "RELIANCE.NS"},
    {"name": "TCS", "ticker": "TCS.NS"},
    {"name": "HDFC Bank", "ticker": "HDFCBANK.NS"},
    {"name": "Jain Irrigation Systems", "ticker": "JISLJALEQS.NS"},
]


@router.get("/search")
def search(q: str):

    q = q.lower()

    results = []

    for stock in STOCK_DB:

        name = stock["name"].lower()
        ticker = stock["ticker"].lower()

        # ✅ fuzzy match
        if q in name or q in ticker:
            results.append(stock)

    return {"results": results[:10]}
