#!/usr/bin/env python3
"""Sanitizer script to clean and repair corrupted legacy cloze brackets in English decks."""

import json
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
ENGLISH_DECKS_DIR = BASE_DIR / "decks" / "03_Languages" / "English"


def repair_cloze_text(text: str) -> str:
    if not isinstance(text, str):
        return text

    # 1. Repair double-nested clozes like {c1::{{c1::value}}}} to {{c1::value}}
    # Loop to handle recursive nesting if any
    while True:
        new_text = re.sub(r"\{c\d+::(\{\{c\d+::.*?\}\})\}+", r"\1", text)
        if new_text == text:
            break
        text = new_text

    # 2. Repair single-braced clozes like {c1::value} to {{c1::value}}
    # Ensure we don't match standard double-braced clozes
    text = re.sub(r"(?<!\{)\{c(\d+)::([^}]+)\}(?!\})", r"{{c\1::\2}}", text)

    return text


def clean_card_content(card: dict) -> int:
    repaired_count = 0
    content = card.get("content", {})
    if not isinstance(content, dict):
        return 0

    # Fields that might contain cloze tags
    fields_to_check = ["text", "gap_text", "prompt", "explanation", "usage", "spanish"]
    for field in fields_to_check:
        if field in content and isinstance(content[field], str):
            original = content[field]
            cleaned = repair_cloze_text(original)
            if cleaned != original:
                content[field] = cleaned
                repaired_count += 1

    return repaired_count


def main():
    print(f"[*] Starting legacy cloze syntax cleanup in: {ENGLISH_DECKS_DIR}")
    if not ENGLISH_DECKS_DIR.exists():
        print(f"[-] Error: English decks directory not found: {ENGLISH_DECKS_DIR}")
        return

    total_files_scanned = 0
    total_cards_scanned = 0
    total_repairs = 0

    for root, _, files in os.walk(ENGLISH_DECKS_DIR):
        for file in files:
            if file.endswith(".json") and file != "index.json" and file != "manifest.json":
                file_path = Path(root) / file
                total_files_scanned += 1
                
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        cards = json.load(f)
                    except Exception as e:
                        print(f"[-] Error parsing {file_path}: {e}")
                        continue

                file_repaired = False
                for card in cards:
                    if isinstance(card, dict):
                        total_cards_scanned += 1
                        repairs = clean_card_content(card)
                        if repairs > 0:
                            total_repairs += repairs
                            file_repaired = True

                if file_repaired:
                    # Save back the clean file
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(cards, f, indent=2, ensure_ascii=False)
                    print(f"  [repaired] {file_path.relative_to(BASE_DIR)}")

    print("\n[+] Cleanup Finished!")
    print(f"    Files scanned: {total_files_scanned}")
    print(f"    Cards scanned: {total_cards_scanned}")
    print(f"    Total field repairs made: {total_repairs}")


if __name__ == "__main__":
    main()
