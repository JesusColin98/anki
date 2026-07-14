import json

with open("decks/index.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for deck in data["decks"]:
    deck_name = deck["deck"]
    path = deck["path"]
    if any(prefix in deck_name for prefix in ["04_Social", "05_Soft", "06_Business"]):
        print(f"Deck: {deck_name}\n  Path: {path}\n  Cards: {deck['cards_count']}")
