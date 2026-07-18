#!/usr/bin/env python3
"""Migration script to convert legacy Job Interview cards to T21_InterviewPrep format using Gemini 2.5 Pro."""

import json
import os
import sys
import time
import requests
from pathlib import Path
from typing import List, Dict, Any

# Setup sys.path to find local modules
BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from template_engine import build_card
from gemini_provider import get_gemini_url

DECKS_DIR = BASE_DIR / "decks"
TARGET_DECK_FILE = DECKS_DIR / "03_Languages" / "English" / "Real_World_Scenarios" / "interview_and_career_pitching.json"

# Strict loop and token safety limits
MAX_MIGRATIONS = 8  # Limit migrations to prevent token consumption / rate limits
RATE_LIMIT_SLEEP = 3.0  # Seconds to wait between API calls
MAX_RETRIES = 3  # For exponential backoff
CONSECUTIVE_FAILURES_LIMIT = 3


def call_gemini_to_upgrade_card(legacy_card: dict) -> Dict[str, Any]:
    """Uses Gemini 2.5 Pro to upgrade a flat vocabulary card into a rich T21 Interview Prep structure."""
    url = get_gemini_url("gemini-2.5-pro")
    
    content_text = legacy_card.get("content", {}).get("text", "")
    content_usage = legacy_card.get("content", {}).get("usage", "")
    content_exp = legacy_card.get("content", {}).get("explanation", "")
    content_spanish = legacy_card.get("content", {}).get("spanish", "")
    
    system_instruction = (
        "You are an expert corporate communications coach and Anki card designer.\n"
        "Your task is to take a legacy flat vocabulary card regarding a job interview, "
        "and transform it into a rich T21_InterviewPrep card that simulates a real professional interview question.\n\n"
        "Return ONLY a JSON object matching this schema:\n"
        "{\n"
        '  "question": "The open-ended interview question or roleplay prompt (in English, e.g. \'Explain how you handle project scope creep...\')",\n'
        '  "target_persona": "The simulated interviewer profile (e.g. \'VP of Product\', \'Lead Architect\', \'HR Recruiter\')",\n'
        '  "rubric_checkpoints": ["List of 3-4 checkpoints that the answer must verbalize to be successful (e.g. \'Define STAR framework\')"],\n'
        '  "communication_cues": ["List of 2-3 delivery tips (e.g. \'Use a steady, assertive tone\')"],\n'
        '  "follow_up_hooks": ["List of 1-2 possible follow-up questions the interviewer would ask next"],\n'
        '  "explanation": "A model answer or explanation of the best strategic way to answer this question (in English)",\n'
        '  "spanish": "Spanish translation of the prompt and key points"\n'
        "}"
    )

    user_prompt = f"""
    Legacy Card Data:
    - Text: {content_text}
    - Explanation: {content_exp}
    - Usage Examples: {content_usage}
    - Spanish Translation: {content_spanish}

    Upgrade this card to a T21_InterviewPrep structure. Synthesize a practical, open-ended question related to the legacy content.
    Return strictly JSON matching the target schema.
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
    
    backoff = 2.0
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 429:
                print(f"    [!] Rate limited (429). Backing off for {backoff}s...")
                time.sleep(backoff)
                backoff *= 2.0
                continue
            resp.raise_for_status()
            result = resp.json()
            raw_text = result["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(raw_text)
        except Exception as e:
            print(f"    [-] Error on attempt {attempt + 1}: {e}")
            time.sleep(1.0)
            
    raise RuntimeError("Failed to query Gemini after retries")


def main():
    print(f"[*] Starting Interview Prep migration on: {TARGET_DECK_FILE}")
    if not TARGET_DECK_FILE.exists():
        print(f"[-] Target file not found: {TARGET_DECK_FILE}")
        return

    with open(TARGET_DECK_FILE, "r", encoding="utf-8") as f:
        cards = json.load(f)

    migrated_count = 0
    consecutive_failures = 0
    updated_cards = []

    # Let's search for interview candidates
    for i, card in enumerate(cards):
        template = card.get("template", "")
        scenario = card.get("content", {}).get("scenario", "").lower()
        tags = card.get("metadata", {}).get("tags", [])
        
        is_interview_candidate = (
            "job interview" in scenario or 
            "interview" in tags or 
            "careers" in tags or
            "05_interviews" in scenario
        )

        if is_interview_candidate and migrated_count < MAX_MIGRATIONS and template == "T1_Cloze":
            print(f"\n[+] Migrating card {migrated_count+1}/{MAX_MIGRATIONS} (ID: {card['id']})...")
            print(f"    Original Text: {card['content'].get('text')}")
            
            try:
                # Call Gemini to upgrade the card
                upgraded_content = call_gemini_to_upgrade_card(card)
                
                # Reconstruct card with new template
                upgraded_card = {
                    "id": card["id"],  # Preserve original ID to maintain review history!
                    "deck": card["deck"],
                    "template": "T21_InterviewPrep",
                    "metadata": {
                        "difficulty": "advanced",
                        "pillar": "03_Languages",
                        "tags": list(set(tags + ["interview_prep", "active_recall"]))
                    },
                    "content": upgraded_content,
                    "mnemonics": card.get("mnemonics", {}),
                    "interactivity": card.get("interactivity", {})
                }
                
                # Validate the new card structures
                compiled_card = build_card("T21_InterviewPrep", upgraded_card)
                updated_cards.append(compiled_card)
                
                migrated_count += 1
                consecutive_failures = 0
                print(f"    [Success] Card successfully upgraded to T21_InterviewPrep!")
                
                # Safe sleep between calls
                time.sleep(RATE_LIMIT_SLEEP)
            except Exception as e:
                consecutive_failures += 1
                print(f"    [-] Failed to migrate card: {e}", file=sys.stderr)
                updated_cards.append(card)  # keep original
                
                if consecutive_failures >= CONSECUTIVE_FAILURES_LIMIT:
                    print(f"\n[-] Aborting migration loop due to {consecutive_failures} consecutive errors.", file=sys.stderr)
                    # Add remaining cards unchanged and exit
                    updated_cards.extend(cards[i+1:])
                    break
        else:
            updated_cards.append(card)

    if migrated_count > 0:
        # Write back updated deck
        with open(TARGET_DECK_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_cards, f, indent=2, ensure_ascii=False)
        print(f"\n[+] Migration loop finished! Upgraded {migrated_count} cards to T21_InterviewPrep format.")
    else:
        print("\n[-] No candidates migrated.")


if __name__ == "__main__":
    main()
