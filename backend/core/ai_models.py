import os
import json
from openai import OpenAI
import requests

# 🔥 GROQ (fast AI)
groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# 🔥 GEMINI endpoint
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def groq_analysis(prompt):

    try:
        res = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return res.choices[0].message.content

    except Exception as e:
        return f"ERROR: {str(e)}"


def gemini_analysis(prompt):

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }

        response = requests.post(url, json=payload, timeout=20)

        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"ERROR: {str(e)}"
