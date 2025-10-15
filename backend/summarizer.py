import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-2.5-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/{MODEL_NAME}:generateContent"

def summarize_transcript(transcript_text):
    if not GEMINI_API_KEY:
        return "❌ Gemini API key not found. Please set GEMINI_API_KEY in your .env file."

    prompt = f"""
Summarize this meeting transcript briefly in 3–5 bullet points, focusing only on key decisions and main discussion outcomes.

Transcript:
{transcript_text}
"""
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            }
        )
        if response.status_code != 200:
            return f"❌ API Error {response.status_code}: {response.text}"

        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Error generating summary: {e}"

def generate_action_items(transcript_text):
    if not GEMINI_API_KEY:
        return "❌ Gemini API key not found. Please set GEMINI_API_KEY in your .env file."

    prompt = f"""
Summarize this meeting transcript into actionable tasks. List all action items clearly under each person's name(make name as heading).

Transcript:
{transcript_text}
"""
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            }
        )
        if response.status_code != 200:
            return f"❌ API Error {response.status_code}: {response.text}"

        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"❌ Error generating action items: {e}"
