import requests
import xml.etree.ElementTree as ET


def fetch_news(ticker):

    try:
        url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            return []

        root = ET.fromstring(res.content)
        items = root.findall(".//item")

        news = []

        for item in items[:5]:
            news.append({
                "title": item.findtext("title", ""),
                "link": item.findtext("link", ""),
                "summary": "Recent market news related to this stock.",
                "impact": "May affect short-term movement."
            })

        return news

    except Exception as e:
        print("RSS error:", e)
        return []
