import yfinance as yf
from core.market_utils import detect_market, clean_ticker


def get_sector_data(ticker):

    stock = yf.Ticker(ticker)
    info = stock.info or {}

    return {
        "ticker": ticker,
        "sector": info.get("sector", "Unknown"),
        "market": detect_market(ticker),
        "price": info.get("currentPrice"),
        "pe": info.get("trailingPE"),
        "growth": info.get("revenueGrowth"),
        "debt": info.get("debtToEquity"),
        "roe": info.get("returnOnEquity")
    }


def find_sector_peers(universe, base_sector, market):

    peers = []

    for t in universe:

        data = get_sector_data(t)

        if data["sector"] == base_sector and data["market"] == market:
            peers.append(data)

    return peers


def rank_sector_opportunities(peers, base_price):

    ranked = []

    for p in peers:

        score = 50

        if p["growth"] and p["growth"] > 0:
            score += 10

        if p["pe"] and p["pe"] < 25:
            score += 10

        if p["roe"] and p["roe"] > 10:
            score += 10

        if p["price"] and p["price"] < base_price:
            score += 10

        ranked.append({
            **p,
            "score": score
        })

    return sorted(ranked, key=lambda x: x["score"], reverse=True)
