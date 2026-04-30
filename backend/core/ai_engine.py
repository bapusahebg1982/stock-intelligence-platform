import os
import requests
import json
import time

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CACHE = {}
CACHE_TTL = 3600  # 1 hour


def cache_get(key):
    if key in CACHE:
        value, ts = CACHE[key]
        if time.time() - ts < CACHE_TTL:
            return value
    return None


def cache_set(key, value):
    CACHE[key] = (value, time.time())


def call_gemini(prompt):

    cache_key = f"gemini::{hash(prompt)}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        res = requests.post(url, json=payload, timeout=20)

        data = res.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]

        cache_set(cache_key, text)

        return text

    except Exception as e:
        return f"ERROR: {str(e)}"


# -------------------------------
# STOCK AI ANALYSIS
# -------------------------------
def generate_stock_analysis(stock_data):

    prompt = f"""
You are a professional equity research analyst.

Analyze this stock and return STRICT JSON.

Stock:
{json.dumps(stock_data)}

Return:

{{
  "consensus": "BUY / HOLD / SELL",
  "confidence": "HIGH / MEDIUM / LOW",
  "risk": "LOW / MEDIUM / HIGH",

  "simple_reason": "Explain in very simple English for beginners",

  "targets": {{
    "short_term": "price in 1-3 months",
    "long_term": "price in 6-12 months"
  }},

  "detailed_reasoning": [
    "valuation insight",
    "growth insight",
    "technical insight"
  ]
}}

Rules:
- Be realistic (no hype)
- Use price, PE, growth, RSI, trend
- Always valid JSON
"""

    raw = call_gemini(prompt)

    try:
        return json.loads(raw)
    except:
        return {
            "consensus": "HOLD",
            "confidence": "LOW",
            "risk": "UNKNOWN",
            "simple_reason": "AI failed, fallback used",
            "targets": {
                "short_term": None,
                "long_term": None
            },
            "detailed_reasoning": [raw]
        }


# -------------------------------
# SECTOR AI
# -------------------------------
def generate_sector_reason(base, candidate):

    prompt = f"""
Explain in simple English why one stock is better than another.

Base stock:
{json.dumps(base)}

Better stock:
{json.dumps(candidate)}

Return 1 short sentence only.
"""

    return call_gemini(prompt)


# -------------------------------
# BEATEN DOWN AI
# -------------------------------
def generate_beaten_reason(stock):

    prompt = f"""
Explain simply:

1. Why this stock may have fallen
2. Why it could rebound

Stock:
{json.dumps(stock)}

Return 1-2 sentences.
"""

    return call_gemini(prompt)
