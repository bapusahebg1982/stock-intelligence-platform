import os
import requests
import json
import re

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# -----------------------------
# UTIL: extract JSON safely
# -----------------------------
def extract_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        return None
    return None


# -----------------------------
# GEMINI CALL (SAFE)
# -----------------------------
def call_gemini(prompt):

    if not GEMINI_API_KEY:
        return None

    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        res = requests.post(url, json=payload, timeout=15)
        data = res.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        print("Gemini error:", e)
        return None


# -----------------------------
# STOCK ANALYSIS
# -----------------------------
def generate_stock_analysis(stock):

    prompt = f"""
Return ONLY JSON.

Stock:
{stock}

Format:
{{
  "consensus": "BUY | HOLD | SELL",
  "confidence": "HIGH | MEDIUM | LOW",
  "risk": "LOW | MEDIUM | HIGH",
  "simple_reason": "short explanation",
  "targets": {{
    "short_term": number,
    "long_term": number
  }},
  "detailed_reasoning": ["r1","r2","r3"]
}}
"""

    raw = call_gemini(prompt)
    parsed = extract_json(raw) if raw else None

    if parsed:
        return parsed

    # fallback
    price = stock.get("price") or 100

    return {
        "consensus": "HOLD",
        "confidence": "MEDIUM",
        "risk": "MEDIUM",
        "simple_reason": "Balanced risk and reward.",
        "targets": {
            "short_term": round(price * 1.05, 2),
            "long_term": round(price * 1.15, 2)
        },
        "detailed_reasoning": [
            "Valuation is moderate",
            "Growth is stable",
            "Momentum is neutral"
        ]
    }


# -----------------------------
# SECTOR REASONING (FIXED)
# -----------------------------
def generate_sector_reason(base, candidate):

    prompt = f"""
Explain in ONE short sentence why this stock may be better.

Base:
{base}

Candidate:
{candidate}
"""

    raw = call_gemini(prompt)

    if raw:
        return raw.strip()

    return "Better relative valuation or growth potential."


# -----------------------------
# BEATEN DOWN REASONING (FIXED)
# -----------------------------
def generate_beaten_reason(stock):

    prompt = f"""
Explain simply:
1. Why stock fell
2. Why rebound possible

Stock:
{stock}

Keep it short.
"""

    raw = call_gemini(prompt)

    if raw:
        return raw.strip()

    return "Stock corrected significantly and may rebound if fundamentals hold."
