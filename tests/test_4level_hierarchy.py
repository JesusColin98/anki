#!/usr/bin/env python3
"""Unit tests verifying the 4-level deep deck hierarchy structure."""

import json
from pathlib import Path
import unittest
from anki_db_importer import load_all_cards

BASE_DIR = Path(__file__).parent.parent.resolve()
DECKS_DIR = BASE_DIR / "decks"
VALID_PILLARS = {
    "01_Cloud_and_Infrastructure",
    "02_AI_and_Data_Science",
    "03_Languages",
    "04_Social_and_Humanities",
    "05_Soft_Skills_and_Leadership",
    "06_Business_and_Productivity",
}


class Test4LevelHierarchy(unittest.TestCase):

    def test_index_structure_and_depth(self):
        index_file = DECKS_DIR / "index.json"
        self.assertTrue(index_file.exists(), "index.json must exist in decks/")

        with open(index_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertGreater(data["total_decks"], 0)
        self.assertGreater(data["total_cards"], 0)

        for entry in data["decks"]:
            deck_name = entry["deck"]
            parts = deck_name.split("::")
            self.assertEqual(
                len(parts), 4, f"Deck '{deck_name}' must have exactly 4 levels"
            )
            self.assertIn(
                parts[0],
                VALID_PILLARS,
                f"Pillar '{parts[0]}' in '{deck_name}' must be one of {VALID_PILLARS}",
            )

            file_path = BASE_DIR / entry["path"]
            self.assertTrue(
                file_path.exists(), f"Deck file missing: {file_path}"
            )

    def test_load_all_cards(self):
        cards = load_all_cards(base_dir=str(BASE_DIR), flatten=False)
        self.assertGreater(len(cards), 0)

        for card in cards:
            self.assertIn("deck", card)
            parts = card["deck"].split("::")
            self.assertEqual(
                len(parts), 4, f"Card deck '{card['deck']}' must have 4 levels"
            )
            self.assertIn(parts[0], VALID_PILLARS)


if __name__ == "__main__":
    unittest.main()
