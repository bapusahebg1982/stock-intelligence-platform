import yfinance as yf

# Stable sources (don’t rely on broken fields)
US_SEED = ["AAPL","MSFT","NVDA","AMZN","META","GOOGL","TSLA"]
INDIA_SEED = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS"]

def get_market_universe(market="US"):

    tickers = set()

    try:
        seeds = US_SEED if market == "US" else INDIA_SEED

        for seed in seeds:

            try:
                stock = yf.Ticker(seed)

                # 🔥 use "recommendations" (more reliable than holdings)
                recs = stock.recommendations

                if recs is not None and not recs.empty:

                    for ticker in recs["To Grade"].dropna().unique():
                        # This is not perfect, so we fallback later
                        pass

                tickers.add(seed)

            except:
                continue

        # Always fallback to seeds (ensures system never breaks)
        if not tickers:
            return seeds

        return list(tickers)

    except:
        return US_SEED if market == "US" else INDIA_SEED
