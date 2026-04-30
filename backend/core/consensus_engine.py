import json
from core.ai_models import groq_analysis, gemini_analysis


def build_prompt(stock):

    return f"""
You are a stock analyst.

Return STRICT JSON only:

Stock:
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

    groq_raw = groq_analysis(prompt)
    gemini_raw = gemini_analysis(prompt)

    groq = safe_parse(groq_raw)
    gemini = safe_parse(gemini_raw)

    rule = rule_based_ai(stock)

    # 🔥 CONSENSUS LOGIC
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

    confidence = round((buy + (3 - sell)) / 3 * 10, 1)

    return {
        "consensus": final,
        "confidence": confidence,

        "targets": {
            "short_term": groq.get("short_term_target"),
            "long_term": gemini.get("long_term_target")
        },

        "ai_votes": {
            "groq": groq.get("recommendation"),
            "gemini": gemini.get("recommendation"),
            "rule_ai": rule.get("recommendation")
        },

        "reasoning": {
            "groq": groq.get("reasoning"),
            "gemini": gemini.get("reasoning"),
            "rule": rule.get("reasoning")
        },

        "risk": groq.get("risk", "medium")
    }


def rule_based_ai(stock):

    score = stock.get("score", 50)

    if score > 70:
        return {
            "recommendation": "BUY",
            "reasoning": "Strong fundamentals & technicals"
        }
    elif score < 40:
        return {
            "recommendation": "SELL",
            "reasoning": "Weak signals detected"
        }

    return {
        "recommendation": "HOLD",
        "reasoning": "Neutral conditions"
    }
