import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from generator import render_t8_card, render_t9_card, RULE_CATALOG
from card_validator import sanitize_and_validate_card

# Map rule filename to rule number
FILE_TO_RULE = {
    "00_Minimal_Pairs.json": 0,
    "01_Cluster_Elision.json": 1,
    "03_Glottal_Stop.json": 3,
    "04_Nasal_T_Deletion.json": 4,
    "06_Resyllabification.json": 6,
    "07_H_Dropping.json": 7,
    "08_Schwa_Reduction.json": 8,
    "09_Linking_R.json": 9,
    "10_Lexical_Chunks.json": 10,
}

DIR_PATH = BASE_DIR / "decks" / "03_Languages" / "English" / "Phonetics" / "Connected_Speech_Patterns"

def run():
    for fname, rule_num in FILE_TO_RULE.items():
        p = DIR_PATH / fname
        if not p.exists():
            print(f"Skipping {fname} (not found)")
            continue
            
        print(f"Rendering {fname}...")
        with open(p, "r", encoding="utf-8") as f:
            raw_cards = json.load(f)
            
        rule_info = RULE_CATALOG[rule_num]
        rendered_cards = []
        
        for i, raw in enumerate(raw_cards):
            # Check if already rendered
            if "text" in raw and "explanation" in raw:
                print(f"  Card {i} already rendered.")
                rendered_cards.append(raw)
                continue
                
            try:
                # Add default fields if missing
                if rule_num == 0:
                    card = render_t8_card(raw, rule_info)
                else:
                    # Provide defaults for missing fields in basic scaffold
                    if "ipa_transcription" not in raw:
                        raw["ipa_transcription"] = ""
                    if "phonetic_breakdown" not in raw:
                        raw["phonetic_breakdown"] = raw.get("spanish", "")
                    card = render_t9_card(raw, rule_info)
                    
                is_valid, cleaned, errs = sanitize_and_validate_card(card)
                if not is_valid:
                    print(f"  Card {i} validation errors: {errs}")
                rendered_cards.append(cleaned)
            except Exception as e:
                print(f"  Error rendering card {i}: {e}")
                
        with open(p, "w", encoding="utf-8") as f:
            json.dump(rendered_cards, f, indent=2, ensure_ascii=False)
        print(f"  Saved {len(rendered_cards)} rendered cards to {fname}")

if __name__ == "__main__":
    run()
