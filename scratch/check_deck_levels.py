import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
DECKS_DIR = BASE_DIR / "decks"

def check():
    mismatches = []
    for p in DECKS_DIR.glob("**/*.json"):
        if p.name == "index.json":
            continue
        try:
            with open(p, "r", encoding="utf-8") as f:
                cards = json.load(f)
            if not cards:
                continue
            deck_name = cards[0].get("deck", "")
            parts = deck_name.split("::")
            if len(parts) != 4:
                mismatches.append((p.relative_to(BASE_DIR), deck_name, len(parts)))
        except Exception as e:
            print(f"Error checking {p.name}: {e}")
            
    print(f"Found {len(mismatches)} mismatches:")
    for path, deck, count in mismatches:
        print(f"  Path: {path}\n    Deck: {deck} ({count} levels)\n")

if __name__ == "__main__":
    check()
