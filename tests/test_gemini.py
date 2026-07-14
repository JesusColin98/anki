#!/usr/bin/env python3
"""Isolated test script for Gemini 2.5 Pro card generation.

Tests the connection to Gemini developer API and prints the generated cards.
"""

import sys
from pathlib import Path

# Ensure root is in sys.path
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from gemini_provider import generate_anki_cards_gemini

def main():
    print("[*] Running isolated test for Gemini 2.5 Pro...")
    sample_text = (
        "Principal Component Analysis (PCA) is an unsupervised learning technique used for "
        "dimensionality reduction. It works by projecting the data onto orthogonal axes that maximize "
        "variance, known as principal components. The first principal component accounts for the largest "
        "possible variance in the dataset."
    )
    deck_name = "02_AI_and_Data_Science::Classical_ML::Overview::PCA"
    
    cards = generate_anki_cards_gemini(sample_text, deck_name)
    if cards:
        print("\n[+] SUCCESS! Gemini 2.5 Pro successfully generated and formatted cards:")
        import json
        print(json.dumps(cards, indent=2, ensure_ascii=False))
    else:
        print("\n[-] FAILURE! No cards were generated. Please check the API key in your .env file or the console errors above.")

if __name__ == "__main__":
    main()
