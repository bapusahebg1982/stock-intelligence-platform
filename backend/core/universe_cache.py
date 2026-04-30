import time
from core.universe_builder import build_universe

CACHE = None
LAST_UPDATED = 0

TTL = 86400  # 24 hours


def get_universe():

    global CACHE, LAST_UPDATED

    if CACHE and (time.time() - LAST_UPDATED < TTL):
        return CACHE

    CACHE = build_universe()
    LAST_UPDATED = time.time()

    return CACHE
