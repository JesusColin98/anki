#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path

# Add project root to path for imports
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(str(BASE_DIR))

from template_engine import build_card

PHONETICS_DIR = BASE_DIR / "decks/03_Languages/English/Phonetics_and_Connected_Speech"

def extract_t8_fields(card):
    content = card.get("content", {})
    text = content.get("text", "")
    explanation = content.get("explanation", "")
    spanish = content.get("spanish", "")
    audio_links = content.get("audio_links", {})
    
    # Extract phoneme A & B
    phoneme_a_match = re.search(r'Phoneme A</b>\s*<code>(.*?)</code>', text)
    phoneme_a = phoneme_a_match.group(1).strip() if phoneme_a_match else "/ɪ/"
    
    phoneme_b_match = re.search(r'Phoneme B</b>\s*<code>(.*?)</code>', text)
    if not phoneme_b_match:
        # try to parse from scenario
        scenario = content.get("scenario", "")
        phonemes = re.findall(r'/(.*?)/', scenario)
        if len(phonemes) >= 2:
            phoneme_a = "/" + phonemes[0] + "/"
            phoneme_b = "/" + phonemes[1] + "/"
        else:
            phoneme_b = "/iː/"
    else:
        phoneme_b = phoneme_b_match.group(1).strip()
        
    # Extract ipa_a (the answer to the cloze in text)
    cloze_match = re.search(r'\{\{c\d+::(.*?)\}\}', text)
    ipa_a = cloze_match.group(1).strip() if cloze_match else "short, relaxed, mid-high front vowel"
    
    # Extract ipa_b from explanation
    ipa_b_match = re.search(rf'<b>{re.escape(phoneme_b)}</b>\s*—\s*(.*?)(?:<br>|\n)', explanation)
    if not ipa_b_match:
        ipa_b_match = re.search(r'<b>/.*?/</b>\s*—\s*(.*?)(?:<br>|\n)', explanation)
    ipa_b = ipa_b_match.group(1).strip() if ipa_b_match else "long, tense, high front vowel"
    
    # Extract word_pairs from the table in explanation
    word_pairs = []
    rows = re.findall(r'<tr>\s*<td>.*?<b>(.*?)</b></td>\s*<td><code>(.*?)</code></td>\s*<td><b>(.*?)</b></td>\s*<td><code>(.*?)</code></td>\s*</tr>', explanation, re.DOTALL)
    for r in rows:
        word_pairs.append([r[0].strip(), r[2].strip(), r[1].strip(), r[3].strip()])
        
    if not word_pairs:
        # Try a relaxed regex
        rows = re.findall(r'<tr>\s*<td>.*?<b>(.*?)</b>.*?<code>(.*?)</code>.*?<b>(.*?)</b>.*?<code>(.*?)</code>.*?</tr>', explanation, re.DOTALL)
        for r in rows:
            word_pairs.append([r[0].strip(), r[2].strip(), r[1].strip(), r[3].strip()])
            
    muscle_tip = spanish
    
    return {
        "phoneme_a": phoneme_a,
        "phoneme_b": phoneme_b,
        "ipa_a": ipa_a,
        "ipa_b": ipa_b,
        "word_pairs": word_pairs,
        "muscle_tip": muscle_tip,
        "language": "en",
        "audio_links": audio_links
    }

def extract_t9_fields(card):
    content = card.get("content", {})
    text = content.get("text", "")
    explanation = content.get("explanation", "")
    spanish = content.get("spanish", "")
    audio_links = content.get("audio_links", {})
    
    # 1. Extract gap_text
    gap_text_match = re.search(r'(?:Fill the gap:|Fill the gap:</b>)<br>\s*(.*)', text, re.IGNORECASE | re.DOTALL)
    if gap_text_match:
        gap_text = gap_text_match.group(1).strip()
    else:
        gap_text = text
        
    # 2. Extract full_transcript
    written_match = re.search(r'Written:</b>\s*(.*?)<br>', explanation, re.IGNORECASE)
    if written_match:
        full_transcript = written_match.group(1).strip()
    else:
        # fallback: extract from cloze
        cloze_match = re.search(r'\{\{c\d+::(.*?)\}\}', gap_text)
        full_transcript = cloze_match.group(1) if cloze_match else "unknown"
        
    # 3. Extract connected_form
    native_match = re.search(r'color:#FF6B35;font-weight:bold;">(.*?)</span>', explanation, re.IGNORECASE)
    if not native_match:
        native_match = re.search(r'Native speed:</b>\s*<span[^>]*>(.*?)</span>', explanation, re.IGNORECASE | re.DOTALL)
    
    if native_match:
        connected_form = re.sub(r'<[^>]*>', '', native_match.group(1)).strip()
    else:
        connected_form = "unknown"
        
    # 4. Extract rules_applied
    rules = []
    rules_section = re.search(r'Rules applied:</b>\s*<ul>(.*?)</ul>', explanation, re.IGNORECASE | re.DOTALL)
    if rules_section:
        rules = re.findall(r'<code>(.*?)</code>', rules_section.group(1))
    if not rules:
        rules = [card["deck"].split("::")[-1].replace("_", " ")]
        
    return {
        "full_transcript": full_transcript,
        "connected_form": connected_form,
        "gap_text": gap_text,
        "rules_applied": rules,
        "language": "en",
        "audio_links": audio_links,
        "spanish": spanish
    }

def main():
    print("=== REFACTORING PHONETICS TEMPLATES ===")
    if not PHONETICS_DIR.exists():
        print(f"Directory {PHONETICS_DIR} not found.")
        sys.exit(1)
        
    for file_path in PHONETICS_DIR.glob("*.json"):
        print(f"Processing: {file_path.name}...")
        
        with open(file_path, "r", encoding="utf-8") as f:
            cards = json.load(f)
            
        refactored_cards = []
        converted_count = 0
        
        for card in cards:
            if card.get("template") == "T1_Cloze":
                tags = card.get("metadata", {}).get("tags", [])
                scenario = card.get("content", {}).get("scenario", "")
                
                # Check if it is a minimal pair card
                if "minimal_pair" in tags or "Minimal Pair" in scenario or file_path.name == "00_minimal_pairs.json":
                    try:
                        extracted = extract_t8_fields(card)
                        flat_data = {
                            "deck": card.get("deck"),
                            "id": card.get("id"),
                            "difficulty": card.get("metadata", {}).get("difficulty", "intermediate"),
                            "tags": card.get("metadata", {}).get("tags", []),
                            **extracted
                        }
                        compiled = build_card("T8_MinimalPair", flat_data)
                        refactored_cards.append(compiled)
                        converted_count += 1
                        continue
                    except Exception as e:
                        print(f"Warning: Failed to convert card {card.get('id')} to T8: {e}")
                
                # Check if it is a connected speech/listening card
                elif any(k in scenario.lower() for k in ["listening", "connected speech", "connected_speech", "flap_t", "cluster", "glottal", "elision", "reduction", "rhythm", "nasal", "yod", "coalescence", "resyllabification", "h_dropping", "linking", "lexical", "dark", "intrusive", "glide", "unreleased", "stop", "syllabic", "flap_d", "pre_glottalization", "auxiliary", "speech"]):
                    try:
                        extracted = extract_t9_fields(card)
                        flat_data = {
                            "deck": card.get("deck"),
                            "id": card.get("id"),
                            "difficulty": card.get("metadata", {}).get("difficulty", "intermediate"),
                            "tags": card.get("metadata", {}).get("tags", []),
                            **extracted
                        }
                        compiled = build_card("T9_ListeningChunk", flat_data)
                        refactored_cards.append(compiled)
                        converted_count += 1
                        continue
                    except Exception as e:
                        print(f"Warning: Failed to convert card {card.get('id')} to T9: {e}")
            
            # Keep as is if not matching or already converted
            refactored_cards.append(card)
            
        print(f"Converted {converted_count} / {len(cards)} cards in {file_path.name}")
        
        # Save file back
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(refactored_cards, f, indent=2, ensure_ascii=False)

    print("[SUCCESS] All phonetics cards refactored successfully.")

if __name__ == "__main__":
    main()
