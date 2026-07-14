#!/usr/bin/env python3
"""Gemini LLM Provider for generating high-quality Anki cards.

Communicates with Gemini Developer API to produce structured Wozniak-compliant cards.
"""

import json
import os
import requests
from typing import List, Dict, Any

from pathlib import Path

def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("GEMINI_API_KEY="):
                    return line.strip().split("=", 1)[1].strip().strip("'\"")
    return ""

GEMINI_API_KEY = get_api_key()
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"

def generate_anki_cards_gemini(prompt_text: str, deck_name: str) -> List[Dict[str, Any]]:
    """Calls Gemini API to generate structured, high-quality Anki cards from input text."""
    system_instruction = (
        "You are an expert Anki card generator. Generate a list of highly atomic cards "
        "following Wozniak's 20 Rules of Formulating Knowledge. Each card must target exactly one fact "
        "using a cloze deletion. You must respond with a JSON object containing a 'cards' key with an array of objects. "
        "Each card object must have: 'deck', 'scenario', 'text', 'explanation', 'usage', 'spanish', 'tags'."
    )
    
    user_prompt = f"""
    Analyze the following technical content and extract high-value atomic facts.
    Create between 2 to 5 high-quality Anki Cloze deletion cards for this content.

    Rules for fields:
    1. 'deck': Must be exactly "{deck_name}".
    2. 'scenario': Descriptive category + situation prefix with an emoji (e.g. "Cloud Security 🔒: IAM Authorization").
    3. 'text': The card front with exactly one balanced cloze deletion (e.g., "The {{c1::least privilege}} principle..."). Keep it concise and atomic (1 fact per card).
    4. 'explanation': A thorough explanation of 'why' it works (minimum 2 or 3 sentences, 20+ characters).
    5. 'usage': A structured HTML list containing key takeaways, example commands, or code (e.g., "<ul><li><b>Tip</b>: ...</li></ul>").
    6. 'spanish': A natural Spanish translation of the text and context.
    7. 'tags': A list of relevant lowercase tags.

    Content to analyze:
    ---
    {prompt_text}
    ---

    Format the output strictly as a JSON object:
    {{
      "cards": [
        {{
          "deck": "{deck_name}",
          "scenario": "...",
          "text": "...",
          "explanation": "...",
          "usage": "...",
          "spanish": "...",
          "tags": ["tag1", "tag2"]
        }}
      ]
    }}
    """

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"{system_instruction}\n\n{user_prompt}"}]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }

    headers = {"Content-Type": "application/json"}

    print(f"[+] Invoking Gemini API for deck '{deck_name}'...")
    try:
        resp = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        
        # Extract response text
        content = result["candidates"][0]["content"]["parts"][0]["text"]
        data = json.loads(content)
        
        cards = data.get("cards", data) if isinstance(data, dict) else data
        if not isinstance(cards, list):
            # Try to handle fallback structures
            if isinstance(data, dict) and "deck" in data:
                cards = [data]
            else:
                cards = []
        
        # Add deck name to any cards that missed it
        for card in cards:
            if isinstance(card, dict):
                card["deck"] = deck_name

        return cards
    except Exception as e:
        print(f"[-] Gemini API card generation error: {e}")
        return []

if __name__ == "__main__":
    sample_text = (
        "Principal Component Analysis (PCA) is an unsupervised learning technique used for "
        "dimensionality reduction. It works by projecting the data onto orthogonal axes that maximize "
        "variance, known as principal components. The first principal component accounts for the largest "
        "possible variance in the dataset."
    )
    cards = generate_anki_cards_gemini(sample_text, "02_AI_and_Data_Science::Classical_ML::Overview::PCA")
    print(json.dumps(cards, indent=2, ensure_ascii=False))
