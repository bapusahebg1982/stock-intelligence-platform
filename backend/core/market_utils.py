US_INDICATORS = [".NS", ".BO"]  # India suffixes (NSE/BSE)


def detect_market(ticker: str) -> str:

    ticker = ticker.upper()

    if any(x in ticker for x in US_INDICATORS):
        return "INDIA"

    return "US"


def clean_ticker(ticker: str) -> str:
    return ticker.upper().replace(".NS", "").replace(".BO", "")
