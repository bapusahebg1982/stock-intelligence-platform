import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_analysis(stock):

    try:
        prompt = build_prompt(stock)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional stock analyst. Always return STRICT JSON only."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )

        text = response.choices[0].message.content

        return parse_json(text)

    except Exception as e:
        return {
            "error": str(e)
        }


# 🔥 STRONG PROMPT (forces JSON)
def build_prompt(stock):

    return f"""
Analyze the stock below and return ONLY JSON.

Stock Data:
Ticker: {stock['ticker']}
Price: {stock['price']}
RSI: {stock['technicals']['rsi']}
Trend: {stock['technicals']['trend']}
PE Ratio: {stock['fundamentals']['pe']}
Revenue Growth: {stock['fundamentals']['revenue_growth']}
1Y High: {stock['high_low']['1y_high']}
1Y Low: {stock['high_low']['1y_low']}

Return STRICT JSON in this exact format:

{{
  "recommendation": "BUY or HOLD or SELL",
  "short_term_target": number,
  "long_term_target": number,
  "timeframe": "e.g. 3-6 months",
  "reasoning": "simple explanation for retail investor",
  "risks": "key risks",
  "confidence": number (1-10)
}}

Rules:
- No text outside JSON
- Targets must be realistic numbers
- Keep reasoning simple and clear
"""


# 🔥 ROBUST PARSER
def parse_json(text):

    try:
        # clean markdown if model returns ```json
        text = text.strip()

        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]

        return json.loads(text)

    except Exception:
        # fallback (important in production)
        return {
            "recommendation": "UNKNOWN",
            "short_term_target": None,
            "long_term_target": None,
            "timeframe": None,
            "reasoning": text,
            "risks": "Parsing failed",
            "confidence": None
        }
