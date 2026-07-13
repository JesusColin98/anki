#!/usr/bin/env python3
"""Migrate monolithic anki_cards_database.json into nested decks/ directory structure.

Maps double-colon deck names (e.g., 'English::01_Daily_Life::Coffee_Shop') to
nested JSON files on disk ('decks/English/01_Daily_Life/Coffee_Shop.json').
"""

import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.resolve()
MONOLITH_JSON = BASE_DIR / "anki_cards_database.json"
DECKS_DIR = BASE_DIR / "decks"


def main():
  if not MONOLITH_JSON.exists():
    print(f"Error: {MONOLITH_JSON} does not exist.", file=sys.stderr)
    sys.exit(1)

  with open(MONOLITH_JSON, "r", encoding="utf-8") as f:
    cards = json.load(f)

  print(f"Loaded {len(cards)} total cards from monolith JSON.")

  deck_map = {}
  for card in cards:
    deck_name = card.get("deck", "Default")
    deck_map.setdefault(deck_name, []).append(card)

  DECKS_DIR.mkdir(parents=True, exist_ok=True)

  index_entries = []
  total_written = 0

  for deck_name, deck_cards in sorted(deck_map.items()):
    rel_path = deck_name.replace("::", "/") + ".json"
    target_file = DECKS_DIR / rel_path
    target_file.parent.mkdir(parents=True, exist_ok=True)

    with open(target_file, "w", encoding="utf-8") as f:
      json.dump(deck_cards, f, indent=2, ensure_ascii=False)

    print(f"  [+] Wrote {len(deck_cards):2d} cards -> decks/{rel_path}")
    total_written += len(deck_cards)
    index_entries.append({
        "deck": deck_name,
        "path": f"decks/{rel_path}",
        "cards_count": len(deck_cards),
    })

  # Write global index file
  index_file = DECKS_DIR / "index.json"
  index_data = {
      "total_cards": total_written,
      "total_decks": len(deck_map),
      "decks": index_entries,
  }
  with open(index_file, "w", encoding="utf-8") as f:
    json.dump(index_data, f, indent=2, ensure_ascii=False)

  print(
      f"\nMigration Complete! Split {total_written} cards across"
      f" {len(deck_map)} subdeck files."
  )
  print(f"Index created at: {index_file}")


if __name__ == "__main__":
  main()
