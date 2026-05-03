import json
import os

FILE = "universe.json"


def load_universe():

    # 🔥 HARD FALLBACK if file missing
    if not os.path.exists(FILE):
        return {
            "US": [
                {"name": "Apple", "ticker": "AAPL"},
                {"name": "Microsoft", "ticker": "MSFT"},
                {"name": "Tesla", "ticker": "TSLA"}
            ],
            "INDIA": [
                {"name": "Reliance", "ticker": "RELIANCE.NS"},
                {"name": "TCS", "ticker": "TCS.NS"},
                {"name": "HDFC Bank", "ticker": "HDFCBANK.NS"}
            ]
        }

    with open(FILE, "r") as f:
        return json.load(f)


def get_us():
    return load_universe()["US"]


def get_india():
    return load_universe()["INDIA"]
