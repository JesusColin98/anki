import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
DECKS_DIR = BASE_DIR / "decks"
MONOLITH_JSON = BASE_DIR / "anki_cards_database.json"

def rebuild():
    print(f"Scanning {DECKS_DIR} for JSON files...")
    
    deck_files = []
    for root, dirs, files in os.walk(DECKS_DIR):
        for f in files:
            if f.endswith('.json') and f != 'index.json':
                deck_files.append(Path(root) / f)
                
    print(f"Found {len(deck_files)} deck files.")
    
    all_cards = []
    index_entries = []
    
    for df in sorted(deck_files):
        # Calculate relative path
        rel_path = df.relative_to(BASE_DIR)
        rel_path_str = str(rel_path).replace('\\', '/')
        
        with open(df, 'r', encoding='utf-8') as f:
            try:
                cards = json.load(f)
            except Exception as e:
                print(f"Error reading {df}: {e}")
                continue
                
        if not cards:
            print(f"Warning: {df} is empty.")
            continue
            
        # Inspect first card to determine deck name
        deck_name = cards[0].get('deck')
        if not deck_name:
            print(f"Warning: No deck name found in first card of {df}")
            continue
            
        # Ensure all cards in this file have the correct deck name and required fields
        for card in cards:
            card['deck'] = deck_name
            if 'usage' not in card:
                card['usage'] = ""
            if 'scenario' not in card:
                card['scenario'] = "Book Concept 📚"
            if 'tags' not in card:
                card['tags'] = []
            
        # Save back updated card list (just to be clean)
        with open(df, 'w', encoding='utf-8') as f:
            json.dump(cards, f, indent=2, ensure_ascii=False)
            
        all_cards.extend(cards)
        index_entries.append({
            "deck": deck_name,
            "path": rel_path_str,
            "cards_count": len(cards)
        })
        
    # Write global index.json
    index_data = {
        "total_cards": len(all_cards),
        "total_decks": len(index_entries),
        "decks": index_entries
    }
    
    index_file = DECKS_DIR / "index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
        
    # Write monolith JSON database
    with open(MONOLITH_JSON, 'w', encoding='utf-8') as f:
        json.dump(all_cards, f, indent=2, ensure_ascii=False)
        
    print("\n=== REBUILD INDEX COMPLETE ===")
    print(f"Total decks: {len(index_entries)}")
    print(f"Total cards: {len(all_cards)}")
    print(f"Saved index to: {index_file}")
    print(f"Saved database to: {MONOLITH_JSON}")

if __name__ == "__main__":
    rebuild()
