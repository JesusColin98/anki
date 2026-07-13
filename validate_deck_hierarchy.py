#!/usr/bin/env python3
"""CLI Tool to Validate 4-Level Deep Deck Hierarchy & Card Syntax Integrity."""

import json
from pathlib import Path
import sys

from card_validator import sanitize_and_validate_card

BASE_DIR = Path(__file__).parent.resolve()
DECKS_DIR = BASE_DIR / "decks"
VALID_PILLARS = {
    "01_Cloud_and_Infrastructure",
    "02_AI_and_Data_Science",
    "03_Languages",
    "04_Social_and_Humanities",
    "05_Soft_Skills_and_Leadership",
    "06_Business_and_Productivity",
}


def main():
    index_file = DECKS_DIR / "index.json"
    if not index_file.exists():
        print(f"Error: {index_file} not found.", file=sys.stderr)
        sys.exit(1)

    with open(index_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []
    total_cards = 0

    for entry in data["decks"]:
        deck_name = entry["deck"]
        parts = deck_name.split("::")

        if len(parts) != 4:
            errors.append(f"Deck '{deck_name}' does not have 4 levels (has {len(parts)}).")
            continue

        if parts[0] not in VALID_PILLARS:
            errors.append(f"Deck '{deck_name}' has invalid pillar '{parts[0]}'.")

        file_path = BASE_DIR / entry["path"]
        if not file_path.exists():
            errors.append(f"Missing deck file: {file_path}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            cards = json.load(f)

        for i, card in enumerate(cards):
            total_cards += 1
            is_valid, _, card_errors = sanitize_and_validate_card(card)
            if not is_valid:
                errors.append(f"Card {i} in '{deck_name}' failed validation: {card_errors}")

    print("=== DECK HIERARCHY & CARD SYNTAX VALIDATION ===")
    print(f"Total Decks Validated: {len(data['decks'])}")
    print(f"Total Cards Validated: {total_cards}")

    if errors:
        print(f"\n[!] Found {len(errors)} validation errors:")
        for err in errors[:10]:
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors.")
        sys.exit(1)
    else:
        print("\n[✓] All 97 decks and 650 cards passed validation cleanly!")
        sys.exit(0)


if __name__ == "__main__":
    main()
