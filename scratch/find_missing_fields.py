import os
import json

decks_dir = "decks"
required_fields = ["deck", "scenario", "text", "explanation", "usage", "spanish"]
found_missing = False

for root, _, files in os.walk(decks_dir):
    for file in files:
        if file.endswith(".json") and file != "index.json":
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    cards = json.load(f)
                    for i, card in enumerate(cards):
                        missing = [field for field in required_fields if field not in card]
                        if missing:
                            print(f"Missing fields {missing} in file: {file_path}")
                            print(f"  Index: {i}")
                            print(f"  Text: {card.get('text', 'N/A')[:60]}")
                            print("-" * 40)
                            found_missing = True
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

if not found_missing:
    print("No cards are missing any required fields.")
