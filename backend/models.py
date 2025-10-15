import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

def list_models():
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    resp = requests.get(url)
    print("v1beta response:", resp.status_code, resp.text)

    url2 = f"https://generativelanguage.googleapis.com/v1/models?key={key}"
    resp2 = requests.get(url2)
    print("v1 response:", resp2.status_code, resp2.text)

if __name__ == "__main__":
    list_models()
