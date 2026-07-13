import urllib.request
import json
import sys

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
    except urllib.error.URLError as e:
        print("Error connecting to AnkiConnect. Is Anki running?", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def clean_duplicates():
    print("Finding all notes of model 'Engaging_Cloze_Model' in Anki...")
    note_ids = invoke('findNotes', query='note:Engaging_Cloze_Model')
    print(f"Found {len(note_ids)} notes in Anki.")
    
    # 1. Retrieve note details in batches
    print("Retrieving note details...")
    note_details = []
    batch_size = 500
    for i in range(0, len(note_ids), batch_size):
        batch = note_ids[i:i+batch_size]
        details = invoke('notesInfo', notes=batch)
        note_details.extend(details)
        
    # 2. Extract first card ID for each note to find its deck name
    print("Extracting card IDs for deck matching...")
    card_to_note = {}
    card_ids = []
    for note in note_details:
        if note.get('cards'):
            first_card = note['cards'][0]
            card_ids.append(first_card)
            card_to_note[first_card] = note['noteId']
            
    # 3. Retrieve card details in batches to get deckName
    print("Retrieving card details (deck names)...")
    card_details = []
    for i in range(0, len(card_ids), batch_size):
        batch = card_ids[i:i+batch_size]
        details = invoke('cardsInfo', cards=batch)
        card_details.extend(details)
        
    # Map noteId to deckName
    note_to_deck = {}
    for card in card_details:
        note_id = card['note']
        note_to_deck[note_id] = card['deckName']
        
    print("Analyzing notes for duplicates...")
    # Group notes by (deckName, Text)
    seen = {}
    to_delete = []
    
    for note in note_details:
        note_id = note['noteId']
        deck_name = note_to_deck.get(note_id, "Unknown_Deck")
        text_field = note['fields'].get('Text', {}).get('value', '').strip()
        
        # Unique key for grouping
        key = (deck_name, text_field)
        
        if key in seen:
            to_delete.append(note_id)
        else:
            seen[key] = note_id
            
    print(f"Found {len(to_delete)} duplicate notes to delete out of {len(note_ids)} total notes.")
    
    if to_delete:
        # Delete notes in batches of 100
        delete_batch_size = 100
        for i in range(0, len(to_delete), delete_batch_size):
            batch = to_delete[i:i+delete_batch_size]
            print(f"Deleting batch of {len(batch)} duplicate notes...")
            invoke('deleteNotes', notes=batch)
        print("Duplicate cleanup complete!")
    else:
        print("No duplicate notes found.")

if __name__ == "__main__":
    clean_duplicates()
