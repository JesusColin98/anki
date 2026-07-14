import os
import sys
import json
import time
import re
from google import genai
from google.genai import types

# Add parent directory to path so we can import card_validator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from card_validator import sanitize_and_validate_card

# Configurations
INPUT_FILE = "scratch/extracted_memory_cards.json"
DECKS_DIR = "decks"
PROJECT_ID = "384412501694"
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.5-flash"
BATCH_SIZE = 15

# Map books to their 4-level deck name and relative file path
DECK_MAP = {
    # 1. Productivity & Learning
    "A Mind For Numbers": {
        "deck": "06_Business_and_Productivity::Books_Path::Productivity::03_Learning_Productivity",
        "path": "decks/06_Business_and_Productivity/Books_Path/Productivity/03_Learning_Productivity.json"
    },
    "Make_It_Stick": {
        "deck": "06_Business_and_Productivity::Books_Path::Productivity::03_Learning_Productivity",
        "path": "decks/06_Business_and_Productivity/Books_Path/Productivity/03_Learning_Productivity.json"
    },
    "Ultralearning": {
        "deck": "06_Business_and_Productivity::Books_Path::Productivity::03_Learning_Productivity",
        "path": "decks/06_Business_and_Productivity/Books_Path/Productivity/03_Learning_Productivity.json"
    },
    "Become a SuperLearner": {
        "deck": "06_Business_and_Productivity::Books_Path::Productivity::04_Memory_and_Superlearning",
        "path": "decks/06_Business_and_Productivity/Books_Path/Productivity/04_Memory_and_Superlearning.json"
    },
    "Building a Second Brain": {
        "deck": "06_Business_and_Productivity::Books_Path::Productivity::05_Personal_Organization",
        "path": "decks/06_Business_and_Productivity/Books_Path/Productivity/05_Personal_Organization.json"
    },
    "How to Take Smart Notes": {
        "deck": "06_Business_and_Productivity::Books_Path::Productivity::05_Personal_Organization",
        "path": "decks/06_Business_and_Productivity/Books_Path/Productivity/05_Personal_Organization.json"
    },
    "Essentialism": {
        "deck": "06_Business_and_Productivity::Books_Path::Productivity::06_Habits_and_Finitude",
        "path": "decks/06_Business_and_Productivity/Books_Path/Productivity/06_Habits_and_Finitude.json"
    },
    "Four Thousand Weeks": {
        "deck": "06_Business_and_Productivity::Books_Path::Productivity::06_Habits_and_Finitude",
        "path": "decks/06_Business_and_Productivity/Books_Path/Productivity/06_Habits_and_Finitude.json"
    },
    "Tiny Habits": {
        "deck": "06_Business_and_Productivity::Books_Path::Productivity::06_Habits_and_Finitude",
        "path": "decks/06_Business_and_Productivity/Books_Path/Productivity/06_Habits_and_Finitude.json"
    },
    # 2. Memory & Mnemonics
    "How to Develop a Brilliant Memory": {
        "deck": "04_Social_and_Humanities::Psychology::Cognitive_Psychology::02_Memory_Systems",
        "path": "decks/04_Social_and_Humanities/Psychology/Cognitive_Psychology/02_Memory_Systems.json"
    },
    "Memory Craft": {
        "deck": "04_Social_and_Humanities::Psychology::Cognitive_Psychology::02_Memory_Systems",
        "path": "decks/04_Social_and_Humanities/Psychology/Cognitive_Psychology/02_Memory_Systems.json"
    },
    "Moonwalking with Einstein": {
        "deck": "04_Social_and_Humanities::Psychology::Cognitive_Psychology::02_Memory_Systems",
        "path": "decks/04_Social_and_Humanities/Psychology/Cognitive_Psychology/02_Memory_Systems.json"
    },
    "The Art Of Memory": {
        "deck": "04_Social_and_Humanities::Psychology::Cognitive_Psychology::02_Memory_Systems",
        "path": "decks/04_Social_and_Humanities/Psychology/Cognitive_Psychology/02_Memory_Systems.json"
    },
    "The Memory Book": {
        "deck": "04_Social_and_Humanities::Psychology::Cognitive_Psychology::02_Memory_Systems",
        "path": "decks/04_Social_and_Humanities/Psychology/Cognitive_Psychology/02_Memory_Systems.json"
    },
    "Unlimited Memory": {
        "deck": "04_Social_and_Humanities::Psychology::Cognitive_Psychology::02_Memory_Systems",
        "path": "decks/04_Social_and_Humanities/Psychology/Cognitive_Psychology/02_Memory_Systems.json"
    },
    # 3. Sales Methodologies
    "Fanatical Prospecting": {
        "deck": "06_Business_and_Productivity::Books_Path::Sales::02_Sales_Methodologies",
        "path": "decks/06_Business_and_Productivity/Books_Path/Sales/02_Sales_Methodologies.json"
    },
    "Gap Selling": {
        "deck": "06_Business_and_Productivity::Books_Path::Sales::02_Sales_Methodologies",
        "path": "decks/06_Business_and_Productivity/Books_Path/Sales/02_Sales_Methodologies.json"
    },
    "Objections": {
        "deck": "06_Business_and_Productivity::Books_Path::Sales::02_Sales_Methodologies",
        "path": "decks/06_Business_and_Productivity/Books_Path/Sales/02_Sales_Methodologies.json"
    },
    "SPIN Selling": {
        "deck": "06_Business_and_Productivity::Books_Path::Sales::02_Sales_Methodologies",
        "path": "decks/06_Business_and_Productivity/Books_Path/Sales/02_Sales_Methodologies.json"
    },
    "The Challenger Sale": {
        "deck": "06_Business_and_Productivity::Books_Path::Sales::02_Sales_Methodologies",
        "path": "decks/06_Business_and_Productivity/Books_Path/Sales/02_Sales_Methodologies.json"
    }
}

# Initialize GenAI Client
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION
)

def call_gemini_with_retry(prompt, system_instruction):
    consecutive_failures = 0
    max_retries = 5
    
    for attempt in range(max_retries):
        try:
            # Respect rate limit
            time.sleep(1)
            
            resp = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1,
                    response_mime_type="application/json"
                )
            )
            return resp.text
        except Exception as e:
            consecutive_failures += 1
            print(f"[-] API error on attempt {attempt+1}/{max_retries}: {e}", flush=True)
            if consecutive_failures >= 3:
                print("[-] Fatal error: 3 consecutive failures encountered. Aborting script.", flush=True)
                sys.exit(1)
            # Exponential backoff
            sleep_time = 2 ** attempt
            print(f"    Backing off for {sleep_time} seconds...", flush=True)
            time.sleep(sleep_time)
            
    print("[-] Failed to get response after maximum retries.", flush=True)
    return None

def process_batch(batch_cards, book_name, deck_name):
    system_instruction = (
        "You are an expert Anki card generator. Convert the input cards into structured JSON format matching this schema:\n"
        "[\n"
        "  {\n"
        "    \"deck\": \"<Pillars::Category::Subcategory::DeckName>\",\n"
        "    \"scenario\": \"<Categoría Corta>: <Contexto o Situación con Emoji>\",\n"
        "    \"text\": \"Oración principal con exactamente un {{c1::<Concepto Clave>}} enfocado.\",\n"
        "    \"explanation\": \"Desglose de 2 a 3 oraciones respondiendo por qué funciona el concepto o la intuición detrás de él.\",\n"
        "    \"usage\": \"<ul><li><b>Uso/Punto clave 1</b>: ...</li><li><b>Uso/Punto clave 2</b>: ...</li></ul>\",\n"
        "    \"spanish\": \"Traducción al español de la oración en 'text', manteniendo el cloze {{c1::...}} exactamente en la misma palabra traducida.\",\n"
        "    \"tags\": [\"books_path\", \"learning_productivity\"]\n"
        "  }\n"
        "]\n"
        "Important rules:\n"
        "1. For term_def cards, make the term the cloze deletion inside a descriptive definition.\n"
        "2. For qa_bold or double_colon cards, convert them into a natural sentence where the key part is cloze deleted.\n"
        "3. Ensure the 'spanish' field translates the 'text' field accurately and keeps the cloze deletion.\n"
        "4. Return ONLY a valid JSON array of card objects. Do not wrap in markdown blocks."
    )
    
    prompt = f"Convert these {len(batch_cards)} cards for the book '{book_name}' under deck '{deck_name}':\n{json.dumps(batch_cards, indent=2)}"
    
    response_text = call_gemini_with_retry(prompt, system_instruction)
    if not response_text:
        return []
        
    try:
        # Clean any markdown packaging if present
        clean_json = response_text.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
        clean_json = clean_json.strip()
        
        cards = json.loads(clean_json)
        # Handle dict wrapping like {"cards": [...]}
        if isinstance(cards, dict) and "cards" in cards:
            cards = cards["cards"]
            
        if isinstance(cards, list):
            return cards
    except Exception as e:
        print(f"[-] JSON parse error on response: {e}", flush=True)
        print("Response received:", response_text, flush=True)
        
    return []

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[-] Input file {INPUT_FILE} not found.", flush=True)
        sys.exit(1)
        
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        extracted_data = json.load(f)
        
    # Group books by their target path so we write to each file only once or progressively
    path_groups = {}
    for book_name, file_entries in extracted_data.items():
        if book_name not in DECK_MAP:
            print(f"[*] Skipping {book_name} (not in DECK_MAP)", flush=True)
            continue
            
        target_info = DECK_MAP[book_name]
        path = target_info["path"]
        if path not in path_groups:
            path_groups[path] = []
            
        # Flatten all cards for this book
        for entry in file_entries:
            for card in entry["cards"]:
                card["book"] = book_name
                card["source_file"] = entry["file"]
                path_groups[path].append(card)
                
    print(f"[+] Grouped cards into {len(path_groups)} files to process.", flush=True)
    
    for path, all_cards in path_groups.items():
        print(f"\n======================================", flush=True)
        print(f"[+] Processing file: {path} ({len(all_cards)} cards total)", flush=True)
        
        # Load existing cards to preserve them
        existing_cards = []
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    existing_cards = json.load(f)
                print(f"[+] Loaded {len(existing_cards)} pre-existing cards.", flush=True)
            except Exception as e:
                print(f"[-] Warning: Failed to load {path}: {e}. Starting fresh.", flush=True)
                
        # Split into batches
        batches = [all_cards[i:i + BATCH_SIZE] for i in range(0, len(all_cards), BATCH_SIZE)]
        new_cards = []
        
        for batch_idx, batch in enumerate(batches):
            print(f"    Batch {batch_idx+1}/{len(batches)} ({len(batch)} cards)...", flush=True)
            # Find the deck name and book name for the first card in the batch
            book_name = batch[0]["book"]
            deck_name = DECK_MAP[book_name]["deck"]
            
            generated_cards = process_batch(batch, book_name, deck_name)
            
            # Validate and sanitize each card
            validated_count = 0
            for card in generated_cards:
                # Force correct deck name
                card["deck"] = deck_name
                
                is_valid, cleaned_card, validation_errors = sanitize_and_validate_card(card)
                if is_valid:
                    new_cards.append(cleaned_card)
                    validated_count += 1
                else:
                    print(f"        [-] Card failed validation, errors: {validation_errors}", flush=True)
                    # Attempt simple repairs or fallback
                    if cleaned_card.get("deck") and cleaned_card.get("text") and cleaned_card.get("spanish") and cleaned_card.get("explanation"):
                        # If it just lacks cloze, add one around first word or skip
                        if "INVALID_CLOZE_TAGS" in str(validation_errors) or "No valid Cloze" in str(validation_errors):
                            # Try putting first word in cloze
                            text = cleaned_card["text"]
                            words = text.split()
                            if words:
                                cleaned_card["text"] = f"{{{{c1::{words[0]}}}}} " + " ".join(words[1:])
                        # Validate again
                        is_valid_now, cleaned_card_now, _ = sanitize_and_validate_card(cleaned_card)
                        if is_valid_now:
                            new_cards.append(cleaned_card_now)
                            validated_count += 1
                            
            print(f"        [+] Validated {validated_count}/{len(generated_cards)} cards from batch.", flush=True)
            
        # Merge and save
        # Avoid duplicate cards based on 'text'
        seen_texts = {c["text"].lower().strip() for c in existing_cards}
        unique_new_cards = []
        for c in new_cards:
            t = c["text"].lower().strip()
            if t not in seen_texts:
                seen_texts.add(t)
                unique_new_cards.append(c)
                
        merged = existing_cards + unique_new_cards
        
        # Ensure parent directories exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)
            
        print(f"[+] Saved. Total cards in {path}: {len(merged)} (Added {len(unique_new_cards)} new cards)", flush=True)

if __name__ == "__main__":
    main()
