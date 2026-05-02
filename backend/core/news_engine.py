import requests
import xml.etree.ElementTree as ET
from core.ai_engine import call_gemini


def fetch_news(ticker):

    try:
        url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"

        res = requests.get(url, timeout=10)
        root = ET.fromstring(res.content)

        items = root.findall(".//item")

        news = []

        for item in items[:5]:
            title = item.find("title").text
            link = item.find("link").text

            news.append({
                "title": title,
                "link": link
            })

        return news

    except:
        return []


def analyze_news(news_list):

    if not news_list:
        return []

    try:
        prompt = f"""
You are a financial analyst.

Analyze these news headlines and return JSON:

{news_list}

Return:

[
  {{
    "title": "...",
    "summary": "1 line summary",
    "sentiment": "POSITIVE / NEGATIVE / NEUTRAL",
    "impact": "Explain why this matters for stock price"
  }}
]

Rules:
- Keep simple
- Be realistic
- Always valid JSON
"""

        result = call_gemini(prompt)

        import json
        return json.loads(result)

    except:
        return news_list
