#!/usr/bin/env python3
"""Tech MBA Card Generator.

Loops through the 200 subtopics defined in scratch/mba_taxonomy.json and calls the
Gemini 2.5 Pro API to generate exactly 10 high-value, Wozniak-compliant Anki cards for each.
Implements rate limiting, exponential backoff, error limit, and a resumable state.
"""

import os
import sys
import json
import time
from pathlib import Path
import requests

# Setup path to import local modules
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from template_engine import build_card
from gemini_provider import get_api_key

TAXONOMY_FILE = BASE_DIR / "scratch" / "mba_taxonomy.json"
STATE_FILE = BASE_DIR / "scratch" / "generate_mba_state.json"
LOG_FILE = BASE_DIR / "scratch" / "generate_mba.log"
DECKS_DIR = BASE_DIR / "decks"

MAX_RETRIES = 5
RETRY_BACKOFF = 3.0  # base backoff factor
RATE_LIMIT_DELAY = 0.5  # seconds between successful requests (local model)
CONSECUTIVE_FAILURE_LIMIT = 3


def log_message(message: str):
    """Logs a message to stdout and the log file."""
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    full_msg = f"{timestamp} {message}"
    print(full_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")


def load_state() -> dict:
    """Loads the progress state or initializes it."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log_message(f"[-] Error loading state file: {e}. Resetting state.")
    return {"completed_subtopics": [], "cards_generated": 0}


def save_state(state: dict):
    """Saves the progress state."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def get_deck_file_path(deck_name: str) -> Path:
    """Maps the 4-level deck name to a file path under decks/."""
    parts = deck_name.split("::")
    # Example: 06_Business_and_Productivity::Business::MBA_Strategy::02_Corporate_Strategy_and_Scale
    # maps to decks/06_Business_and_Productivity/Business/MBA_Strategy/02_Corporate_Strategy_and_Scale.json
    return DECKS_DIR / Path(*parts[0:3]) / f"{parts[3]}.json"


def call_gemini_api(deck_name: str, module_name: str, subtopic_name: str, subtopic_focus: str, api_key: str) -> list:
    """Calls local Ollama API to generate exactly 10 cards using Qwen 2.5 14B model."""
    url = "http://localhost:11434/v1/chat/completions"
    
    system_instruction = (
        "You are an expert MBA professor and Anki card designer. Generate a list of exactly 10 premium, "
        "high-value flashcards for the given subtopic. You must respond with a JSON object containing a 'cards' key with an array of objects. "
        "Each card object must specify its 'template' type and contain all the required fields for that template."
    )
    
    prompt = f"""
    DECK: {deck_name}
    MODULE: {module_name}
    SUBTOPIC: {subtopic_name}
    FOCUS: {subtopic_focus}
    
    Generate exactly 10 highly educational Anki cards for this subtopic.
    Choose the most appropriate template from the list below for each card to maximize pedagogical value:

    1. "T1_Cloze" (General concepts and facts):
       Required fields: "template", "text" (contains one {{c1::cloze}}), "explanation" (minimum 2 sentences), "spanish", "scenario" (short situation + emoji).
    
    2. "T2_DualCoding" (Visual processes, workflows, structures using Mermaid diagrams):
       Required fields: "template", "concept" (the process name), "mermaid_code" (valid flowchart/diagram), "explanation" (detailed context), "spanish".
       *Note: Mermaid arrows must be valid (-->). Double quote labels with special chars, e.g. A["Label (Extra)"].*

    3. "T4_Scenario" (Conversational skills, negotiations, stakeholder conflict, sales pitch):
       Required fields: "template", "scenario" (situation + emoji), "target_phrase" (what to say, with a {{c1::cloze}} deletion), "usage" (HTML list: <ul><li>...</li></ul>), "spanish".

    4. "T5_MathJax" (Formulas, metrics, accounting ratios):
       Required fields: "template", "concept", "formula_latex" (e.g. \\frac{{LTV}}{{CAC}}), "variable_breakdown" (HTML list of variables: <li>...</li>).

    5. "T6_Quiz" (Case-study multiple choice questions):
       Required fields: "template", "question", "options" (array of 4 choices), "correct_option" (must match one option), "rationale" (why it is correct).

    6. "T11_ExecutivePitch" (Executive communication, leadership pitching, shadowing):
       Required fields: "template", "speaker", "source_context", "transcript_excerpt" (speech excerpt), "pitch_analysis" (intonation/pitch curve description), "pause_map", "shadowing_script" (phonetic shadowing helper), "leadership_technique" (technique name).

    Format the output strictly as a JSON object:
    {{
      "cards": [
        {{
          "template": "T1_Cloze" | "T2_DualCoding" | "T4_Scenario" | "T5_MathJax" | "T6_Quiz" | "T11_ExecutivePitch",
          ... (fields required by the chosen template)
        }}
      ]
    }}
    """
    
    payload = {
        "model": "qwen2.5:14b",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"}
    }
    
    retries = 0
    while retries < MAX_RETRIES:
        try:
            resp = requests.post(url, json=payload, timeout=120)
            resp.raise_for_status()
            result = resp.json()
            
            # Extract content text
            content_text = result["choices"][0]["message"]["content"]
            data = json.loads(content_text)
            
            cards = data.get("cards", [])
            if not isinstance(cards, list):
                if isinstance(data, list):
                    cards = data
                else:
                    log_message(f"[-] Invalid format returned: 'cards' is not a list. Retrying...")
                    retries += 1
                    continue
                
            return cards
            
        except Exception as e:
            sleep_time = RETRY_BACKOFF ** (retries + 1)
            log_message(f"[-] Local Ollama request failed: {e}. Retrying in {sleep_time:.1f}s...")
            time.sleep(sleep_time)
            retries += 1
            
    raise RuntimeError(f"Failed to generate cards after {MAX_RETRIES} attempts.")


def append_cards_to_deck(deck_name: str, cards: list):
    """Appends cards to the deck JSON file, preserving and validating existing cards."""
    file_path = get_deck_file_path(deck_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    existing_cards = []
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_cards = json.load(f)
                if not isinstance(existing_cards, list):
                    existing_cards = []
        except Exception as e:
            log_message(f"[-] Error reading existing deck file {file_path}: {e}")
            
    existing_cards.extend(cards)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing_cards, f, indent=2, ensure_ascii=False)


def main():
    log_message("[+] starting MBA Card Generation Factory...")
    
    api_key = get_api_key()
    if not api_key:
        log_message("[-] GEMINI_API_KEY not found in environment or .env file.")
        sys.exit(1)
        
    if not TAXONOMY_FILE.exists():
        log_message(f"[-] Taxonomy file not found at {TAXONOMY_FILE}.")
        sys.exit(1)
        
    with open(TAXONOMY_FILE, "r", encoding="utf-8") as f:
        taxonomy = json.load(f)
        
    state = load_state()
    consecutive_failures = 0
    
    # Flatten taxonomy to subtopics list for linear progress tracking
    flat_subtopics = []
    for deck in taxonomy:
        deck_name = deck["deck"]
        for module in deck["modules"]:
            module_name = module["name"]
            for subtopic in module["subtopics"]:
                subtopic_id = f"{deck_name}::{module_name}::{subtopic['name']}"
                flat_subtopics.append({
                    "id": subtopic_id,
                    "deck_name": deck_name,
                    "module_name": module_name,
                    "subtopic_name": subtopic["name"],
                    "focus": subtopic["focus"]
                })
                
    total_subtopics = len(flat_subtopics)
    log_message(f"[+] Total subtopics in taxonomy: {total_subtopics}. Progress: {len(state['completed_subtopics'])}/{total_subtopics}")
    
    for i, subtopic in enumerate(flat_subtopics):
        subtopic_id = subtopic["id"]
        if subtopic_id in state["completed_subtopics"]:
            continue
            
        log_message(f"--- Subtopic {i+1}/{total_subtopics} ---")
        log_message(f"[+] Subtopic: {subtopic['subtopic_name']}")
        log_message(f"[+] Focus: {subtopic['focus']}")
        log_message(f"[+] Deck: {subtopic['deck_name']}")
        
        try:
            # Call API to generate cards
            raw_cards = call_gemini_api(
                deck_name=subtopic["deck_name"],
                module_name=subtopic["module_name"],
                subtopic_name=subtopic["subtopic_name"],
                subtopic_focus=subtopic["focus"],
                api_key=api_key
            )
            
            # Render and validate cards
            validated_cards = []
            for card_data in raw_cards:
                try:
                    template_type = card_data.get("template")
                    if not template_type:
                        continue
                    
                    card_data["deck"] = subtopic["deck_name"]
                    
                    # build_card does rendering + validation
                    built_card = build_card(template_type, card_data)
                    validated_cards.append(built_card)
                except Exception as card_err:
                    log_message(f"    [-] Card build failed: {card_err}")
            
            if validated_cards:
                append_cards_to_deck(subtopic["deck_name"], validated_cards)
                state["completed_subtopics"].append(subtopic_id)
                state["cards_generated"] += len(validated_cards)
                save_state(state)
                log_message(f"[OK] Generated & saved {len(validated_cards)} cards for {subtopic['subtopic_name']}")
                consecutive_failures = 0  # reset failures
            else:
                log_message(f"[-] No valid cards generated for {subtopic['subtopic_name']}")
                consecutive_failures += 1
                
        except Exception as api_err:
            log_message(f"[-] Fatal error generating subtopic: {api_err}")
            consecutive_failures += 1
            
        if consecutive_failures >= CONSECUTIVE_FAILURE_LIMIT:
            log_message(f"[-] Aborting: Reached {CONSECUTIVE_FAILURE_LIMIT} consecutive failures.")
            sys.exit(1)
            
        # Rate limit safety sleep
        log_message(f"[+] Sleeping for {RATE_LIMIT_DELAY}s between requests...")
        time.sleep(RATE_LIMIT_DELAY)
        
    log_message(f"[+] MBA Card Generation Factory completed successfully! Total cards generated: {state['cards_generated']}")


if __name__ == "__main__":
    main()
