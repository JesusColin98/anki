#!/usr/bin/env python3
import json
import urllib.request
import sys

def anki_invoke(action, **params):
    payload = {"action": action, "version": 6}
    if params:
        payload["params"] = params
    try:
        req = urllib.request.Request("http://localhost:8765", json.dumps(payload).encode("utf-8"))
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            if res.get("error"):
                raise Exception(res["error"])
            return res.get("result")
    except Exception as e:
        print(f"Error calling AnkiConnect: {e}")
        return None

def main():
    print("=== ANKI EMPTY DECKS CLEANUP ===")
    
    # 1. Fetch all decks
    all_decks = anki_invoke("deckNames")
    if not all_decks:
        print("Could not retrieve decks from Anki. Make sure Anki Desktop is running.")
        sys.exit(1)
        
    # 2. Fetch deck stats in a single bulk call
    print("Fetching stats for all decks in bulk...")
    stats = anki_invoke("getDeckStats", decks=all_decks)
    if not stats:
        print("Failed to get deck stats.")
        sys.exit(1)
        
    # Map deck name to card count
    deck_counts = {}
    for info in stats.values():
        deck_counts[info["name"]] = info["total_in_deck"]
        
    empty_decks = []
    
    # 3. Identify empty decks
    for deck in all_decks:
        count = deck_counts.get(deck, 0)
        if count == 0:
            # Check if this deck has subdecks that contain cards
            has_nonempty_subdecks = False
            for potential_sub in all_decks:
                if potential_sub.startswith(f"{deck}::") and potential_sub != deck:
                    if deck_counts.get(potential_sub, 0) > 0:
                        has_nonempty_subdecks = True
                        break
            
            if not has_nonempty_subdecks:
                empty_decks.append(deck)
                
    if not empty_decks:
        print("No empty decks found.")
        sys.exit(0)
        
    print(f"\nFound {len(empty_decks)} empty decks to delete:")
    for deck in empty_decks:
        print(f"  - {deck}")
        
    # 4. Delete the empty decks
    try:
        print("\nDeleting empty decks...")
        anki_invoke("deleteDecks", decks=empty_decks, cardsToo=True)
        print("[SUCCESS] Empty legacy decks deleted successfully.")
    except Exception as e:
        print(f"Error deleting empty decks: {e}")

if __name__ == "__main__":
    main()
