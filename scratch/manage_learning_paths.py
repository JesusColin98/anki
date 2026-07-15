import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
MANIFEST_PATH = BASE_DIR / "decks" / "03_Languages" / "English" / "Variant_Pipeline" / "manifest.json"

def invoke(action, **params):
    payload = {'action': action, 'version': 6}
    if params:
        payload['params'] = params
    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8765', data=req_data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            if res.get('error') is not None:
                raise Exception(res['error'])
            return res['result']
    except urllib.error.URLError:
        print("Error: Could not connect to AnkiConnect. Is Anki running?", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        raise e

def get_learning_path_deck(source_file):
    # Map source JSON files to thematic study objectives
    sf = source_file.replace("\\", "/").lower()
    if "05_interviews" in sf:
        return "03_Languages::English::Learning_Paths::03_Interview_and_Career"
    elif "02_workplace" in sf or "06_phone_calls" in sf:
        return "03_Languages::English::Learning_Paths::02_Workplace_and_Service"
    elif "07_health" in sf or "08_education" in sf:
        return "03_Languages::English::Learning_Paths::04_Academic_and_Health"
    else:
        # Default Daily & Social for 01_Daily_Life, 03_Travel, 04_Social
        return "03_Languages::English::Learning_Paths::01_Daily_and_Social"

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ["--apply", "--restore"]:
        print("Usage: python manage_learning_paths.py [--apply | --restore]")
        print("  --apply   : Reorganizes Anki cards into thematic Learning Paths (Daily, Workplace, Interview, Academic).")
        print("  --restore : Reverts cards in Anki back to their default Variant Pipeline subdecks (Speaking, Listening, etc.).")
        sys.exit(1)
        
    mode = sys.argv[1]
    
    if not MANIFEST_PATH.exists():
        print(f"Error: manifest.json not found at {MANIFEST_PATH}", file=sys.stderr)
        sys.exit(1)
        
    print(f"Loading relationship manifest from {MANIFEST_PATH.name}...")
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    # Map: text_val -> target_deck
    target_mapping = {}
    
    # Read files in variant pipeline to get actual texts of generated cards
    pipeline_dir = MANIFEST_PATH.parent
    for sub in pipeline_dir.iterdir():
        if sub.is_dir():
            for json_file in sub.glob("*.json"):
                with open(json_file, "r", encoding="utf-8") as f:
                    cards = json.load(f)
                for card in cards:
                    # Find relationship item for this card
                    source_id = card.get("source_id")
                    variant_type = card.get("variant_type")
                    match = None
                    for rel in manifest["relationships"]:
                        if rel["source_id"] == source_id and rel["variant_type"] == variant_type:
                            match = rel
                            break
                    
                    if match:
                        text_key = str(card.get("text") or card.get("prompt") or "").strip()
                        if mode == "--apply":
                            target_mapping[text_key] = get_learning_path_deck(match["source_file"])
                        else:
                            # Restore to original Variant Pipeline subdeck
                            target_mapping[text_key] = match["deck"]

    print(f"Mapped {len(target_mapping)} unique cards to their target decks.")

    # Fetch notes in Anki
    print("Fetching notes from Anki...")
    note_ids = invoke('findNotes', query='note:Engaging_Cloze_Model')
    try:
        speaking_ids = invoke('findNotes', query='note:Engaging_Speaking_Model')
        note_ids.extend(speaking_ids)
    except Exception:
        pass
        
    if not note_ids:
        print("No notes found in Anki to reorganize.")
        return
        
    print(f"Fetching details of {len(note_ids)} notes in Anki...")
    notes_details = []
    batch_size = 500
    for i in range(0, len(note_ids), batch_size):
        batch = note_ids[i:i+batch_size]
        details = invoke('notesInfo', notes=batch)
        notes_details.extend(details)
        
    # Get note ID to deck mapping
    card_ids_to_fetch = []
    for note in notes_details:
        if note.get('cards'):
            card_ids_to_fetch.append(note['cards'][0])
            
    card_details = []
    for i in range(0, len(card_ids_to_fetch), batch_size):
        batch = card_ids_to_fetch[i:i+batch_size]
        details = invoke('cardsInfo', cards=batch)
        card_details.extend(details)
        
    note_to_deck = {card['note']: card['deckName'] for card in card_details}

    # Perform deck reassignments
    reassigned_count = 0
    skipped_count = 0
    decks_to_ensure = set(target_mapping.values())
    
    # Ensure target decks exist
    for deck in sorted(list(decks_to_ensure)):
        invoke('createDeck', deck=deck)
        
    print("\nStarting note deck reassignment in Anki...")
    for note in notes_details:
        note_id = note['noteId']
        current_deck = note_to_deck.get(note_id)
        
        # Get key
        text_val = note['fields'].get('Text', {}).get('value', '')
        if not text_val and 'Prompt' in note['fields']:
            text_val = note['fields'].get('Prompt', {}).get('value', '')
        text_val = text_val.strip()
        
        if text_val in target_mapping:
            target_deck = target_mapping[text_val]
            if current_deck != target_deck:
                card_ids = note.get('cards', [])
                if card_ids:
                    invoke('changeDeck', cards=card_ids, deck=target_deck)
                    reassigned_count += 1
            else:
                skipped_count += 1
                
    print(f"\nDone! Reassigned {reassigned_count} cards to new decks, {skipped_count} cards were already in their correct decks.")

if __name__ == "__main__":
    main()
