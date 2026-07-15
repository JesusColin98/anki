import os
import requests
import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))
from gemini_provider import get_api_key

api_key = get_api_key()
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"

system_instruction = (
    "You are an expert MBA professor and Anki card designer. Generate a list of exactly 10 premium, "
    "high-value flashcards for the given subtopic. You must respond with a JSON object containing a 'cards' key with an array of objects. "
    "Each card object must specify its 'template' type and contain all the required fields for that template."
)

prompt = """
DECK: 06_Business_and_Productivity::Business::MBA_Strategy::02_Corporate_Strategy_and_Scale
MODULE: Competitive Advantage & 7 Powers
SUBTOPIC: Scale Economies & Barriers
FOCUS: How scale economies act as barriers to entry, benefit-barrier matrix, and cost advantages.
"""

payload = {
    "contents": [
        {
            "role": "user",
            "parts": [{"text": f"{system_instruction}\n\n{prompt}"}]
        }
    ],
    "generationConfig": {
        "responseMimeType": "application/json",
        "temperature": 0.2
    }
}
headers = {"Content-Type": "application/json"}

try:
    resp = requests.post(url, headers=headers, json=payload, timeout=45)
    print("Status Code:", resp.status_code)
    print("Response Headers:", resp.headers)
    print("Response Body:", resp.text)
except Exception as e:
    print("Error:", e)
