#!/usr/bin/env python3
import json
import os
import sys
import time
import requests
from pathlib import Path

# Add project root to path for imports
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(str(BASE_DIR))

from gemini_provider import GEMINI_API_KEY
from card_validator import sanitize_and_validate_card

LANGUAGES_DIR = BASE_DIR / "decks/03_Languages"
MAX_ENRICH_CARDS = 15  # Strict API loop control

def enrich_card_explanation(concept, text, old_explanation, spanish, language):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured.")
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""
    You are an expert language teacher and memory scientist.
    Analyze the following language card and generate a high-quality, deep, pedagogical explanation.
    
    Language: {language}
    Concept/Word: {concept}
    Sentence/Prompt: {text}
    Current Explanation: {old_explanation}
    Spanish Translation: {spanish}
    
    INSTRUCTIONS:
    1. Explain "why" the concept/word/phrase is used in this context.
    2. Include grammatical details, politeness levels (formal vs. informal), or particles if relevant.
    3. Include etymology, root meanings, or cultural context if helpful.
    4. Propose a short visual mnemonic scene to help anchor the memory.
    5. Write the explanation in English, but format it clearly using basic HTML (e.g. bold <b>, italics <i>, linebreaks <br>).
    6. Minimum explanation length: 2 or 3 sentences (at least 60 characters).
    
    Respond STRICTLY with a JSON object:
    {{
      "explanation": "Your enriched HTML explanation here"
    }}
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.3
        }
    }
    
    resp = requests.post(url, json=payload, timeout=20)
    resp.raise_for_status()
    res = resp.json()
    content = res["candidates"][0]["content"]["parts"][0]["text"]
    data = json.loads(content)
    return data.get("explanation")

def main():
    print("=== STARTING LANGUAGE CONTENT ENRICHMENT ===")
    if not LANGUAGES_DIR.exists():
        print(f"Directory {LANGUAGES_DIR} not found.")
        sys.exit(1)
        
    thin_cards = []
    
    # 1. Scan and identify thin cards
    for root, _, files in os.walk(LANGUAGES_DIR):
        for file in sorted(files):
            if file.endswith(".json") and file not in ["index.json", "manifest.json"]:
                file_path = Path(root) / file
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        cards = json.load(f)
                    for idx, card in enumerate(cards):
                        content = card.get("content", {})
                        explanation = content.get("explanation", "").strip()
                        
                        # Define a thin card: less than 35 characters or matches general template placeholder
                        is_thin = len(explanation) < 35 or "vocabulary for the topic" in explanation.lower()
                        
                        if is_thin and card.get("template") == "T1_Cloze":
                            thin_cards.append({
                                "file_path": file_path,
                                "card_index": idx,
                                "card": card
                            })
                except Exception as e:
                    print(f"Error scanning {file_path}: {e}")
                    
    print(f"Found {len(thin_cards)} thin cards across all language decks.")
    if not thin_cards:
        print("No thin cards found. Exiting.")
        sys.exit(0)
        
    # Limit number of enrichments
    to_enrich = thin_cards[:MAX_ENRICH_CARDS]
    print(f"Running enrichment for {len(to_enrich)} cards to comply with API loop safety bounds.")
    
    consecutive_errors = 0
    enriched_count = 0
    
    # Group by file path so we write changes efficiently
    files_to_update = {}
    
    for idx, item in enumerate(to_enrich):
        file_path = item["file_path"]
        card_index = item["card_index"]
        card = item["card"]
        content = card.get("content", {})
        
        concept = content.get("concept", content.get("text", ""))
        text = content.get("text", "")
        old_explanation = content.get("explanation", "")
        spanish = content.get("spanish", "")
        language = card["deck"].split("::")[1] if "::" in card["deck"] else "English"
        
        print(f"\n[{idx+1}/{len(to_enrich)}] Enriching card in '{file_path.name}': {concept[:30]}...")
        
        try:
            enriched_exp = enrich_card_explanation(concept, text, old_explanation, spanish, language)
            
            # Update card in-memory
            card["content"]["explanation"] = enriched_exp
            
            # Validate card
            is_valid, cleaned_card, val_errors = sanitize_and_validate_card(card)
            if val_errors:
                print(f"Warning: Enrichment validation issues: {val_errors}")
            
            # Record change
            if file_path not in files_to_update:
                files_to_update[file_path] = []
            files_to_update[file_path].append((card_index, cleaned_card))
            
            enriched_count += 1
            consecutive_errors = 0
            time.sleep(1.0)  # Rate limiting safety pause
            
        except Exception as e:
            print(f"Error enriching card: {e}")
            consecutive_errors += 1
            if consecutive_errors >= 3:
                print("Aborting enrichment run due to 3 consecutive API failures.")
                break
                
    # 2. Write changes back to disk
    for file_path, updates in files_to_update.items():
        with open(file_path, "r", encoding="utf-8") as f:
            cards = json.load(f)
            
        for card_index, cleaned_card in updates:
            cards[card_index] = cleaned_card
            
        print(f"Saving {len(updates)} enriched cards to {file_path.name}...")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(cards, f, indent=2, ensure_ascii=False)
            
    print(f"\n[SUCCESS] Enriched {enriched_count} cards successfully.")

if __name__ == "__main__":
    main()
