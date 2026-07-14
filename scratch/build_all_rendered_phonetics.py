import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from scratch.phonetics_db import DATA
from generator import render_t9_card, RULE_CATALOG
from card_validator import sanitize_and_validate_card

DECKS_DIR = BASE_DIR / "decks" / "03_Languages" / "English" / "Phonetics" / "Connected_Speech_Patterns"

def build():
    print(f"Creating parent directories at {DECKS_DIR}...")
    DECKS_DIR.mkdir(parents=True, exist_ok=True)
    
    total_generated = 0
    
    for rule_num, items in DATA.items():
        rule_info = RULE_CATALOG.get(rule_num)
        if not rule_info:
            print(f"[-] No rule info for rule {rule_num}, skipping.")
            continue
            
        print(f"\n[+] Processing Rule {rule_num}: {rule_info['name']} ({len(items)} items)")
        
        rendered_cards = []
        for i, item in enumerate(items):
            # Parse tuple (full_transcript, connected_form, gap_text, spanish)
            full_tx, conn, gap, span = item
            
            # Formulate raw card fields
            raw = {
                "scenario": f"Fast English: {rule_info['name']} 🎧 — Card {i+1}",
                "full_transcript": full_tx,
                "connected_form": conn,
                "ipa_transcription": "", # populated with placeholder or left blank for render fallback
                "gap_text": gap,
                "rules_applied": [rule_info["name"].replace("_", " ")],
                "audio_search_forvo": full_tx.split()[0] if " " in full_tx else full_tx,
                "audio_search_youglish": full_tx,
                "phonetic_breakdown": f"Phonetic transition drill for '{full_tx}' pronounced as '{conn}'.",
                "spanish": span,
                "tier": 1 if i < 10 else (2 if i < 20 else 3)
            }
            
            try:
                rendered = render_t9_card(raw, rule_info)
                
                # Validate the card
                is_valid, cleaned, errs = sanitize_and_validate_card(rendered)
                if not is_valid:
                    print(f"  [!] Card {i+1} failed validation: {errs}")
                    
                rendered_cards.append(cleaned)
            except Exception as e:
                print(f"  [-] Error rendering card {i+1}: {e}")
                
        out_file = DECKS_DIR / rule_info["file"]
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(rendered_cards, f, indent=2, ensure_ascii=False)
            
        print(f"  [OK] Saved {len(rendered_cards)} cards to {out_file.name}")
        total_generated += len(rendered_cards)
        
    print(f"\n[OK] Finished generating phonetics corpus! Total cards: {total_generated}")

if __name__ == "__main__":
    build()
