import json
from core.model_router import call_groq, call_gemini


def build_prompt(stock):

    return f"""
You are a professional stock analyst.

Return ONLY JSON:

Ticker: {stock['ticker']}
Price: {stock['price']}
RSI: {stock['technicals']['rsi']}
Trend: {stock['technicals']['trend']}
PE: {stock['fundamentals']['pe']}

Format:
{{
  "recommendation": "BUY/HOLD/SELL",
  "short_term_target": number,
  "long_term_target": number,
  "reasoning": "simple explanation",
  "risk": "low/medium/high"
}}
"""


def safe_parse(text):

    try:
        text = text.strip()

        if "```" in text:
            text = text.split("```")[1]

        return json.loads(text)

    except:
        return {
            "recommendation": "HOLD",
            "short_term_target": None,
            "long_term_target": None,
            "reasoning": text,
            "risk": "unknown"
        }


def run_multi_ai(stock):

    prompt = build_prompt(stock)

    groq_raw = call_groq(prompt)
    gemini_raw = call_gemini(prompt)

    groq = safe_parse(groq_raw)
    gemini = safe_parse(gemini_raw)

    rule = rule_based(stock)

    votes = [
        groq.get("recommendation"),
        gemini.get("recommendation"),
        rule.get("recommendation")
    ]

    buy = votes.count("BUY")
    sell = votes.count("SELL")

    if buy >= 2:
        final = "BUY"
    elif sell >= 2:
        final = "SELL"
    else:
        final = "HOLD"

    return {
        "consensus": final,
        "confidence": round((buy + (3 - sell)) / 3 * 10, 1),

        "targets": {
            "short_term": groq.get("short_term_target"),
            "long_term": gemini.get("long_term_target")
        },

        "ai_votes": {
            "groq": groq.get("recommendation"),
            "gemini": gemini.get("recommendation"),
            "rule": rule.get("recommendation")
        },

        "reasoning": {
            "groq": groq.get("reasoning"),
            "gemini": gemini.get("reasoning"),
            "rule": rule.get("reasoning")
        },

        "risk": groq.get("risk", "medium")
    }


def rule_based(stock):

    score = stock.get("score", 50)

    if score > 70:
        return {"recommendation": "BUY", "reasoning": "Strong fundamentals"}
    elif score < 40:
        return {"recommendation": "SELL", "reasoning": "Weak signals"}

    return {"recommendation": "HOLD", "reasoning": "Neutral conditions"}
