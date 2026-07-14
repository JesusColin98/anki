import json
import os

with open('temp_additions.json', 'r', encoding='utf-8') as f:
    additions = json.load(f)

print(f"Loaded {len(additions)} additions.")

modified_files = {}

for card in additions:
    deck = card['deck']
    parts = deck.split('::')
    file_path = os.path.join('decks', *parts) + '.json'
    
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
            
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            cards = json.load(f)
        except Exception:
            cards = []
            
    # Check if card text already exists to prevent duplicate addition
    existing_texts = {c['text'].strip().lower() for c in cards}
    if card['text'].strip().lower() not in existing_texts:
        cards.append(card)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(cards, f, indent=2, ensure_ascii=False)
        modified_files[file_path] = modified_files.get(file_path, 0) + 1

print("\nDistribution Summary:")
for path, count in sorted(modified_files.items()):
    print(f"  {path}: Added {count} cards.")
