import time

# Simple in-memory cache (production-ready upgrade later → Redis)

CACHE = {}

# TTL in seconds (15 minutes)
TTL = 900


def get_cache(key):

    if key not in CACHE:
        return None

    data, timestamp = CACHE[key]

    if time.time() - timestamp > TTL:
        del CACHE[key]
        return None

    return data


def set_cache(key, value):

    CACHE[key] = (value, time.time())


def clear_cache():
    CACHE.clear()
