#!/usr/bin/env python3
"""
fix_trivial_cloze.py — Fix trivial cloze deletions (is/are/am) in daily_social deck
=====================================================================================
For cards where the cloze only covers 'is', 'are', or 'am', expands the cloze
to cover the meaningful predicate phrase instead.

Strategy: move cloze from the linking verb to the key content phrase in the sentence.
e.g. "She {{c1::is}} a software engineer" → "She is {{c1::a software engineer}}"
"""
import json, re, sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Specific card IDs to fix (all trivial is/are/am cloze)
TRIVIAL_IDS = {
    "c589f427c5c9469d", "7438025a9ab56535", "693f477b5711fe0c",
    "a13639d75df7cf9f", "bc870610978d2c56", "39f6ce3fa6c58e64",
    "c1da60778ee7244a", "eff97489093edfe4", "beee754b63041b56",
    "a90dfdd650ad0d15",
}

TRIVIAL_VERBS = re.compile(r'\{\{c(\d+)::(is|are|am|Is|Are|Am)\}\}', re.IGNORECASE)

def expand_cloze(text: str) -> str:
    """
    Expand a trivial is/are/am cloze to cover the following predicate.
    'She {{c1::is}} a software engineer' → 'She {{c1::is a software engineer}}'
    '{{c1::Are}} you the new developer?' → '{{c1::Are you}} the new developer?' (kept as-is for question form)
    """
    # Pattern: verb + space + rest of meaningful predicate up to comma or end
    def expand_match(m):
        verb = m.group(2)
        cnum = m.group(1)
        return f'{{{{c{cnum}::{verb}'  # open cloze, will close at next meaningful boundary

    # Simpler approach: find each trivial verb cloze and extend to end of clause
    result = text
    # Replace "{{c1::is}} PREDICATE" → "{{c1::is PREDICATE}}"
    # Only expand if the verb is followed by a space and content (not a punctuation)
    result = re.sub(
        r'\{\{(c\d+)::(is|are|am)\}\}(\s+)([^,\.;]+?)([,\.;]|$)',
        lambda m: f'{{{{{m.group(1)}::{m.group(2)}{m.group(3)}{m.group(4).rstrip()}}}}}{m.group(5)}',
        result,
        flags=re.IGNORECASE
    )
    # For question forms: "{{c1::Are}} you" → keep subject in cloze too
    result = re.sub(
        r'\{\{(c\d+)::(Are|Is)\}\}(\s+)(\w+)',
        lambda m: f'{{{{{m.group(1)}::{m.group(2)}{m.group(3)}{m.group(4)}}}}}',
        result,
        flags=re.IGNORECASE
    )
    return result


def run():
    target = Path(__file__).parent / "decks" / "03_Languages" / "English" / "Real_World_Scenarios" / "daily_and_social_interactions.json"
    cards = json.loads(target.read_text(encoding="utf-8"))

    fixed = 0
    for card in cards:
        if card.get("id") not in TRIVIAL_IDS:
            continue
        content = card.get("content", {})
        text = content.get("text", "")
        if not text:
            continue

        original = text
        new_text = expand_cloze(text)

        if new_text != original:
            content["text"] = new_text
            print(f"[{card['id']}]")
            print(f"  BEFORE: {original}")
            print(f"  AFTER:  {new_text}")
            print()
            fixed += 1

    if fixed:
        target.write_text(json.dumps(cards, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Fixed {fixed} trivial-cloze cards.")


if __name__ == "__main__":
    run()
