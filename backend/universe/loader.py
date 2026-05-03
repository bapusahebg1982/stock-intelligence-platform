import json
import os

UNIVERSE_FILE = "universe.json"


def load_universe():

    if not os.path.exists(UNIVERSE_FILE):
        return {"US": [], "INDIA": []}

    with open(UNIVERSE_FILE, "r") as f:
        return json.load(f)


def get_us():
    return load_universe().get("US", [])


def get_india():
    return load_universe().get("INDIA", [])
