import yfinance as yf

# 🔥 Core index proxies (broad + sector coverage)
US_INDEX_PROXIES = [
    "SPY",   # S&P 500 ETF
    "QQQ",   # Nasdaq
    "DIA",   # Dow
    "IWM"    # Russell 2000
]

INDIA_INDEX_PROXIES = [
    "^NSEI",   # Nifty 50
    "^BSESN"   # Sensex
]


def get_market_universe(market="US"):

    tickers = set()

    try:
        proxies = US_INDEX_PROXIES if market == "US" else INDIA_INDEX_PROXIES

        for proxy in proxies:

            data = yf.Ticker(proxy)

            # 🔥 pull related tickers (approximation)
            info = data.info

            if "holdings" in info:
                for holding in info["holdings"]:
                    tickers.add(holding.get("symbol"))

        # fallback: add popular tickers dynamically
        fallback = get_fallback_tickers(market)
        tickers.update(fallback)

        return list(filter(None, tickers))

    except:
        return get_fallback_tickers(market)


def get_fallback_tickers(market):

    if market == "US":
        return [
            "AAPL","MSFT","NVDA","AMZN","META",
            "GOOGL","TSLA","AMD","NFLX","INTC"
        ]

    else:
        return [
            "RELIANCE.NS","TCS.NS","INFY.NS",
            "HDFCBANK.NS","ICICIBANK.NS"
        ]
