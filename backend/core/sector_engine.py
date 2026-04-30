import yfinance as yf
from core.ai_engine import generate_sector_reason


def get_sector_opportunities(universe, base_ticker):

    try:
        base_info = yf.Ticker(base_ticker).info or {}
        base_sector = base_info.get("sector")

        results = []

        for ticker in universe:

            try:
                info = yf.Ticker(ticker).info or {}

                if info.get("sector") != base_sector:
                    continue

                data = {
                    "ticker": ticker,
                    "price": info.get("currentPrice"),
                    "sector": info.get("sector"),
                    "score": 50
                }

                data["reason"] = generate_sector_reason(base_info, info)

                results.append(data)

            except:
                continue

        return sorted(results, key=lambda x: x["score"], reverse=True)

    except:
        return []
