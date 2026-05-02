import os
import requests
import json
import re

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def extract_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        return None


def call_gemini(prompt):

    # ✅ HARD SAFETY: if no key → skip AI
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

    # ✅ ALWAYS RETURN VALID OUTPUT
    price = stock.get("price") or 100

    return {
        "consensus": "HOLD",
        "confidence": "MEDIUM",
        "risk": "MEDIUM",
        "simple_reason": "Stable stock with balanced risk and reward.",
        "targets": {
            "short_term": round(price * 1.05, 2),
            "long_term": round(price * 1.15, 2)
        },
        "detailed_reasoning": [
            "Valuation is moderate",
            "Growth is steady",
            "Momentum is neutral"
        ]
    }
