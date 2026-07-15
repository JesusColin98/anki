import requests
import json
import os
import sys
from pathlib import Path

# Add project root to path for imports
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(str(BASE_DIR))

from gemini_provider import GEMINI_API_KEY

def main():
    print("API Key exists:", bool(GEMINI_API_KEY))
    
    # Try gemini-2.5-pro
    url_25 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": "Hello"}]}]
    }
    resp = requests.post(url_25, json=payload)
    print("gemini-2.5-pro Status:", resp.status_code)
    try:
        print("gemini-2.5-pro Response:", resp.json())
    except Exception:
        print("gemini-2.5-pro Response Raw:", resp.text)
        
    # Try gemini-1.5-flash (alternative standard model)
    url_15 = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    resp = requests.post(url_15, json=payload)
    print("\ngemini-1.5-flash Status:", resp.status_code)
    try:
        print("gemini-1.5-flash Response:", resp.json())
    except Exception:
        print("gemini-1.5-flash Response Raw:", resp.text)

if __name__ == "__main__":
    main()
