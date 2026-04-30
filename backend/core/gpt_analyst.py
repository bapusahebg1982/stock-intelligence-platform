import os
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
                {"role": "system", "content": "You are a professional stock analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        text = response.choices[0].message.content

        return parse_output(text)

    except Exception as e:
        return {
            "error": str(e)
        }


def build_prompt(stock):

    return f"""
Analyze this stock and give investment recommendation:

Ticker: {stock['ticker']}
Price: {stock['price']}
RSI: {stock['technicals']['rsi']}
Trend: {stock['technicals']['trend']}
PE Ratio: {stock['fundamentals']['pe']}
Revenue Growth: {stock['fundamentals']['revenue_growth']}
1Y High: {stock['high_low']['1y_high']}
1Y Low: {stock['high_low']['1y_low']}

Provide:
1. Recommendation (BUY / HOLD / SELL)
2. Target price (short term)
3. Target price (long term)
4. Timeframe
5. Reasoning (simple + professional)
6. Risks

Return in JSON format.
"""
    

def parse_output(text):

    # 🔥 simple fallback parser (LLM may return text)
    return {
        "raw": text
    }
