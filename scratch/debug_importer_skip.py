import os
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from anki_db_importer import load_all_cards, ensure_model_exists, invoke

def debug():
    cards = load_all_cards()
    print(f"Total cards loaded from JSON: {len(cards)}")
    
    # Query all existing notes in Anki
    existing_note_ids = invoke('findNotes', query='note:Engaging_Cloze_Model')
    try:
        speaking_ids = invoke('findNotes', query='note:Engaging_Speaking_Model')
        existing_note_ids.extend(speaking_ids)
    except Exception:
        pass
        
    print(f"Total notes in Anki: {len(existing_note_ids)}")
    
    # Fetch note details
    notes_details = []
    batch_size = 500
    for i in range(0, len(existing_note_ids), batch_size):
        batch = existing_note_ids[i:i+batch_size]
        details = invoke('notesInfo', notes=batch)
        notes_details.extend(details)
        
    # Get note ID to deck mapping
    card_ids = []
    for note in notes_details:
        if note.get('cards'):
            card_ids.append(note['cards'][0])
            
    card_details = []
    for i in range(0, len(card_ids), batch_size):
        batch = card_ids[i:i+batch_size]
        details = invoke('cardsInfo', cards=batch)
        card_details.extend(details)
        
    note_to_deck = {card['note']: card['deckName'] for card in card_details}
    
    existing_anki_notes = {}
    for note in notes_details:
        note_id = note['noteId']
        deck_name = note_to_deck.get(note_id, "Unknown")
        text_val = note['fields'].get('Text', {}).get('value', '')
        if not text_val and 'Prompt' in note['fields']:
            text_val = note['fields'].get('Prompt', {}).get('value', '')
        text_val = text_val.strip()
        existing_anki_notes[text_val] = {
            'noteId': note_id,
            'deckName': deck_name
        }
        
    # Now check how many cards in JSON are matched or skipped
    matched = 0
    skipped_new = 0
    skipped_existing = 0
    
    for card in cards:
        text_key = str(card.get('text') or card.get('prompt') or '').strip()
        if text_key in existing_anki_notes:
            matched += 1
        else:
            skipped_new += 1
            if skipped_existing < 80:
                print(f"Unmatched Card {skipped_existing+1}: Deck: {card['deck']}, Text: {repr(text_key[:60])}")
                skipped_existing += 1
                    
    print(f"Matched (exist in Anki): {matched}")
    print(f"Unmatched (should be added): {skipped_new}")

if __name__ == "__main__":
    debug()
