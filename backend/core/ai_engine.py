import os
import requests
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def call_gemini(prompt):

    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        res = requests.post(url, json=payload, timeout=20)

        data = res.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"ERROR: {str(e)}"


# -------------------------------
# MAIN AI ANALYSIS
# -------------------------------
def generate_ai_analysis(stock_data):

    prompt = f"""
You are a professional stock analyst.

Analyze the following stock and return STRICT JSON.

Stock Data:
{json.dumps(stock_data)}

Return JSON in this format:

{{
  "consensus": "BUY / HOLD / SELL",
  "confidence": "HIGH / MEDIUM / LOW",
  "risk": "LOW / MEDIUM / HIGH",

  "simple_reason": "Explain in simple English for a beginner",

  "targets": {{
    "short_term": "price target in 1-3 months",
    "long_term": "price target in 6-12 months"
  }},

  "detailed_reasoning": [
    "reason 1",
    "reason 2",
    "reason 3"
  ]
}}

Rules:
- Be realistic (no hype)
- Use valuation, growth, momentum
- Keep explanation simple but useful
- Always return valid JSON
"""

    response = call_gemini(prompt)

    try:
        return json.loads(response)
    except:
        return {
            "consensus": "HOLD",
            "confidence": "LOW",
            "risk": "UNKNOWN",
            "simple_reason": "AI failed to generate response",
            "targets": {
                "short_term": None,
                "long_term": None
            },
            "detailed_reasoning": [response]
        }


# -------------------------------
# SECTOR AI
# -------------------------------
def generate_sector_reason(base, candidate):

    prompt = f"""
Explain in simple English why this stock is better than another.

Base Stock:
{json.dumps(base)}

Better Stock:
{json.dumps(candidate)}

Return ONE sentence only.
"""

    return call_gemini(prompt)


# -------------------------------
# BEATEN DOWN AI
# -------------------------------
def generate_beaten_reason(stock):

    prompt = f"""
Explain in simple English:

1. Why this stock may have fallen
2. Why it could rebound

Stock Data:
{json.dumps(stock)}

Return 1-2 short sentences.
"""

    return call_gemini(prompt)
