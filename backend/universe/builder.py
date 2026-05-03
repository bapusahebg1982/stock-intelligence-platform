import requests
import json

UNIVERSE_FILE = "universe.json"


# -----------------------------
# 🇺🇸 US STOCK UNIVERSE (NASDAQ + NYSE)
# -----------------------------
def fetch_us_universe():
    """
    Uses Stooq free endpoint (no API key required)
    """
    url = "https://raw.githubusercontent.com/datasets/nasdaq-listings/master/data/nasdaq-listed-symbols.csv"

    import pandas as pd
    df = pd.read_csv(url)

    universe = []

    for _, row in df.iterrows():
        universe.append({
            "name": row["Security Name"],
            "ticker": row["Symbol"]
        })

    return universe


# -----------------------------
# 🇮🇳 INDIA UNIVERSE (NSE)
# -----------------------------
def fetch_india_universe():
    """
    NSE equity list (public CSV endpoint)
    """
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

    import pandas as pd
    df = pd.read_csv(url)

    universe = []

    for _, row in df.iterrows():
        universe.append({
            "name": row["NAME OF COMPANY"],
            "ticker": row["SYMBOL"] + ".NS"
        })

    return universe


# -----------------------------
# SAVE UNIVERSE
# -----------------------------
def build_universe():
    us = fetch_us_universe()
    india = fetch_india_universe()

    full = {
        "US": us,
        "INDIA": india
    }

    with open(UNIVERSE_FILE, "w") as f:
        json.dump(full, f)

    return full


if __name__ == "__main__":
    build_universe()
    print("Universe built successfully")
