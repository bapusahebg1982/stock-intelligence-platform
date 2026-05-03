from core.ai_engine import call_gemini


def generate_beaten_insight(ticker, price, drawdown, timeframe):

    prompt = f"""
You are a stock analyst.

Stock: {ticker}
Price: {price}
Drawdown: {drawdown}%
Timeframe: {timeframe}

Return JSON:

{{
  "reason_drop": "why stock fell",
  "reason_opportunity": "why it can recover",
  "confidence": "HIGH/MEDIUM/LOW"
}}

Keep it simple and realistic.
"""

    raw = call_gemini(prompt)

    try:
        import json
        return json.loads(raw)
    except:
        return {
            "reason_drop": "Market correction or sector weakness.",
            "reason_opportunity": "Fundamentals remain stable.",
            "confidence": "MEDIUM"
        }
