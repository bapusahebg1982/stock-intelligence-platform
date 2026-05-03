from fastapi import APIRouter
import yfinance as yf
import difflib

router = APIRouter()

# ✅ REALISTIC UNIVERSAL STOCK MAP (India + US core)
STOCK_DB = [
    # US
    {"name": "Apple", "ticker": "AAPL"},
    {"name": "Microsoft", "ticker": "MSFT"},
    {"name": "Amazon", "ticker": "AMZN"},
    {"name": "Tesla", "ticker": "TSLA"},
    {"name": "NVIDIA", "ticker": "NVDA"},

    # India banks
    {"name": "HDFC Bank", "ticker": "HDFCBANK.NS"},
    {"name": "ICICI Bank", "ticker": "ICICIBANK.NS"},
    {"name": "State Bank of India", "ticker": "SBIN.NS"},
    {"name": "Axis Bank", "ticker": "AXISBANK.NS"},
    {"name": "Bandhan Bank", "ticker": "BANDHANBNK.NS"},

    # others
    {"name": "Reliance Industries", "ticker": "RELIANCE.NS"},
    {"name": "TCS", "ticker": "TCS.NS"},
]


def normalize(text):
    return text.lower().strip()


def score_match(query, name):
    q = normalize(query)
    n = normalize(name)

    if q == n:
        return 100
    if q in n:
        return 80
    if any(word in n for word in q.split()):
        return 60
    return 0


@router.get("/search")
def search(q: str):

    if not q:
        return {"results": []}

    q_norm = normalize(q)

    scored = []

    # 🔥 STEP 1: score ALL matches (no early return)
    for stock in STOCK_DB:
        score = score_match(q_norm, stock["name"])

        if score > 0:
            scored.append({**stock, "score": score})

    # 🔥 STEP 2: sort by BEST match
    scored.sort(key=lambda x: x["score"], reverse=True)

    # 🔥 STEP 3: strict top match only if strong confidence
    if scored and scored[0]["score"] >= 60:
        return {"results": scored[:5]}

    # 🔥 STEP 4: fallback ticker guessing
    try:
        guess = q.upper().replace(" ", "")

        for suffix in ["", ".NS"]:
            ticker = guess + suffix

            stock = yf.Ticker(ticker)
            info = stock.info

            name = info.get("longName") or info.get("shortName")

            if name:
                return {
                    "results": [{"name": name, "ticker": ticker}]
                }

    except:
        pass

    return {"results": []}
