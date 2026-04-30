import os
import requests
import json
from openai import OpenAI

# ---------------------------
# GROQ CLIENT
# ---------------------------
groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ---------------------------
# GROQ CALL
# ---------------------------
def call_groq(prompt):

    try:
        res = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return res.choices[0].message.content

    except Exception as e:
        return f"ERROR: {str(e)}"


# ---------------------------
# GEMINI CALL
# ---------------------------
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

        response = requests.post(url, json=payload, timeout=25)
        data = response.json()

        # DEBUG (keep for now)
        print("GEMINI RESPONSE:", data)

        if "candidates" not in data:
            return f"ERROR: {data}"

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"ERROR: {str(e)}"
