import json
import urllib.request
import urllib.error
import sys
import os
from pathlib import Path

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
        print(f"Error connecting to AnkiConnect. Is Anki running?", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        raise e

def ensure_model_exists():
    models = invoke('modelNames')

    cloze_css = """
.card {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 19px;
    line-height: 1.6;
    color: #2D3748;
    background-color: #F7FAFC;
    padding: 24px;
    max-width: 550px;
    margin: 0 auto;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.cloze {
    font-weight: bold;
    color: #4F46E5;
    background-color: #EEF2FF;
    padding: 2px 8px;
    border-radius: 6px;
}

.scenario-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #718096;
    background-color: #EDF2F7;
    padding: 4px 12px;
    border-radius: 9999px;
    margin-bottom: 16px;
}

hr {
    border: none;
    border-top: 1px solid #E2E8F0;
    margin: 20px 0;
}

.sentence-front {
    font-size: 22px;
    font-weight: 500;
    color: #1A202C;
    margin: 12px 0;
}

.explanation-section {
    background-color: #FFFFFF;
    border-left: 4px solid #4F46E5;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 16px;
    text-align: left;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.explanation-section h3 {
    margin: 0 0 6px 0;
    font-size: 13px;
    color: #4F46E5;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.examples-section {
    background-color: #FFFFFF;
    border-left: 4px solid #10B981;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 16px;
    text-align: left;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.examples-section h3 {
    margin: 0 0 6px 0;
    font-size: 13px;
    color: #10B981;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.examples-section ul {
    margin: 0;
    padding-left: 20px;
    color: #4A5568;
}

.examples-section li {
    margin-bottom: 6px;
}

.examples-section code {
    background-color: #ECFDF5;
    color: #047857;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 14px;
}

details {
    background-color: #EDF2F7;
    padding: 10px 14px;
    border-radius: 8px;
    margin-top: 16px;
    font-size: 15px;
    color: #4A5568;
    cursor: pointer;
    text-align: left;
    transition: background-color 0.2s;
}

details:hover {
    background-color: #E2E8F0;
}

details summary {
    font-weight: 600;
    outline: none;
    user-select: none;
}

details p {
    margin: 8px 0 0 0;
    color: #2D3748;
}

/* Night Mode support */
.nightMode .card {
    color: #E2E8F0;
    background-color: #1A202C;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.nightMode .cloze {
    color: #818CF8;
    background-color: #312E81;
}

.nightMode .scenario-badge {
    color: #A0AEC0;
    background-color: #2D3748;
}

.nightMode hr {
    border-top: 1px solid #2D3748;
}

.nightMode .sentence-front {
    color: #F7FAFC;
}

.nightMode .explanation-section {
    background-color: #2D3748;
    border-left: 4px solid #818CF8;
}

.nightMode .explanation-section h3 {
    color: #818CF8;
}

.nightMode .examples-section {
    background-color: #2D3748;
    border-left: 4px solid #34D399;
}

.nightMode .examples-section h3 {
    color: #34D399;
}

.nightMode .examples-section code {
    background-color: #065F46;
    color: #A7F3D0;
}

.nightMode details {
    background-color: #2D3748;
    color: #A0AEC0;
}

.nightMode details:hover {
    background-color: #4A5568;
}

.nightMode details p {
    color: #E2E8F0;
}
"""

    speaking_css = """
.card {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 19px;
    line-height: 1.6;
    color: #2D3748;
    background-color: #F8FAFC;
    padding: 24px;
    max-width: 620px;
    margin: 0 auto;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.scenario-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #475569;
    background-color: #E2E8F0;
    padding: 4px 12px;
    border-radius: 9999px;
    margin-bottom: 16px;
}

.prompt-block {
    font-size: 22px;
    font-weight: 600;
    color: #0F172A;
    margin-bottom: 16px;
}

.audio-player {
    background: #EFF6FF;
    border-left: 4px solid #2563EB;
    padding: 12px 16px;
    border-radius: 8px;
    margin: 12px 0;
}

.practice-link {
    margin-top: 10px;
}

.practice-link a {
    color: #2563EB;
    font-weight: 600;
    text-decoration: none;
}

.practice-link a:hover {
    text-decoration: underline;
}

.nightMode .card {
    background-color: #1E293B;
    color: #E2E8F0;
}

.nightMode .prompt-block {
    color: #F8FAFC;
}

.nightMode .audio-player {
    background: #1E3A8A;
    border-left-color: #60A5FA;
}
"""

    models_to_create = [
        {
            "model_name": "Engaging_Cloze_Model",
            "is_cloze": True,
            "css": cloze_css,
            "front_template": """<div class=\"scenario-badge\">{{Scenario}}</div>
<div class=\"sentence-front\">{{cloze:Text}}</div>""",
            "back_template": """<div class=\"scenario-badge\">{{Scenario}}</div>
<div class=\"sentence-front\">{{cloze:Text}}</div>
<hr>
<div class=\"explanation-section\">
    <h3>Meaning & Context</h3>
    {{Explanation}}
</div>
<div class=\"examples-section\">
    <h3>Key Takeaways & Examples</h3>
    {{Usage_Examples}}
</div>
<details>
    <summary>Show Spanish Translation</summary>
    <p>{{Spanish_Translation}}</p>
</details>
{{Audio}}""",
            "fields": ["Text", "Scenario", "Explanation", "Usage_Examples", "Spanish_Translation", "Audio"],
        },
        {
            "model_name": "Engaging_Speaking_Model",
            "is_cloze": False,
            "css": speaking_css,
            "front_template": """<div class=\"scenario-badge\">{{Scenario}}</div>
<div class=\"prompt-block\">{{Prompt}}</div>
{{Audio}}
{{Practice_Link}}""",
            "back_template": """<div class=\"scenario-badge\">{{Scenario}}</div>
<div class=\"prompt-block\">{{Prompt}}</div>
{{Audio}}
<div class=\"practice-link\">{{Practice_Link}}</div>
<hr>
<div class=\"explanation-section\">
    <h3>Meaning & Context</h3>
    {{Explanation}}
</div>
<div class=\"examples-section\">
    <h3>Practice Notes</h3>
    {{Usage_Examples}}
</div>
<details>
    <summary>Show Spanish Translation</summary>
    <p>{{Spanish_Translation}}</p>
</details>
<div class=\"audio-player\">{{Recording_Hint}}</div>""",
            "fields": ["Prompt", "Scenario", "Explanation", "Usage_Examples", "Spanish_Translation", "Audio", "Practice_Link", "Recording_Hint"],
        },
    ]

    for spec in models_to_create:
        model_name = spec["model_name"]
        if model_name in models:
            print(f"Model '{model_name}' already exists.")
            continue

        print(f"Creating custom model '{model_name}'...")
        invoke(
            'createModel',
            modelName=model_name,
            inOrderFields=spec["fields"],
            isCloze=spec["is_cloze"],
            cardTemplates=[{
                "Name": "Main Template",
                "Front": spec["front_template"],
                "Back": spec["back_template"],
            }],
            css=spec["css"],
        )
    print("Models created successfully.")

def load_all_cards(base_dir="."):
    decks_dir = os.path.join(base_dir, "decks")
    cards = []
    if os.path.exists(decks_dir):
        print(f"Reading cards from nested decks directory: {decks_dir}...")
        for root, _, files in os.walk(decks_dir):
            for file in sorted(files):
                if file.endswith(".json") and file != "index.json":
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            deck_cards = json.load(f)
                            rel_path = os.path.relpath(file_path, decks_dir)
                            derived_deck = str(Path(rel_path).with_suffix("")).replace(os.sep, "::")
                            for card in deck_cards:
                                if "deck" not in card or not card["deck"]:
                                    card["deck"] = derived_deck
                            cards.extend(deck_cards)
                    except Exception as e:
                        print(f"Warning: Could not load {file_path}: {e}", file=sys.stderr)
        print(f"Loaded {len(cards)} total cards from decks/ directory tree.")
        return cards
    
    monolith_file = os.path.join(base_dir, "anki_cards_database.json")
    if os.path.exists(monolith_file):
        print(f"Reading database {monolith_file}...")
        with open(monolith_file, "r", encoding="utf-8") as f:
            return json.load(f)
            
    print("Error: Neither decks/ directory nor anki_cards_database.json found.", file=sys.stderr)
    sys.exit(1)

def import_database():
    cards = load_all_cards()
        
    # De-duplicate cards in the database itself if any exist
    unique_cards = []
    seen_db_keys = set()
    for card in cards:
        key = (card['deck'], card['text'].strip())
        if key not in seen_db_keys:
            seen_db_keys.add(key)
            unique_cards.append(card)
        else:
            print(f"Warning: Ignored duplicate card in JSON database: Deck '{card['deck']}', Text '{card['text'][:60]}...'")
            
    cards = unique_cards
    ensure_model_exists()
    
    # Collect and create unique decks
    decks = set(card['deck'] for card in cards)
    for deck in sorted(decks):
        print(f"Ensuring deck '{deck}' exists...")
        invoke('createDeck', deck=deck)
        
    # Query all existing notes of our custom model in Anki
    print("\nFetching existing notes from Anki...")
    existing_note_ids = invoke('findNotes', query='note:Engaging_Cloze_Model')
    
    # Fetch details of existing notes in batches
    existing_notes_details = []
    batch_size = 500
    for i in range(0, len(existing_note_ids), batch_size):
        batch = existing_note_ids[i:i+batch_size]
        details = invoke('notesInfo', notes=batch)
        existing_notes_details.extend(details)
        
    # Extract first card for each note to find its deck
    card_ids = []
    for note in existing_notes_details:
        if note.get('cards'):
            card_ids.append(note['cards'][0])
            
    # Fetch card details in batches to get deck names
    card_details = []
    for i in range(0, len(card_ids), batch_size):
        batch = card_ids[i:i+batch_size]
        details = invoke('cardsInfo', cards=batch)
        card_details.extend(details)
        
    # Map note ID to deck name
    note_to_deck = {}
    for card in card_details:
        note_to_deck[card['note']] = card['deckName']
        
    # Create mapping of Text -> (noteId, deckName, fields, tags, cards)
    existing_anki_notes = {}
    for note in existing_notes_details:
        note_id = note['noteId']
        deck_name = note_to_deck.get(note_id, "Unknown")
        text_val = note['fields'].get('Text', {}).get('value', '').strip()
        existing_anki_notes[text_val] = {
            'noteId': note_id,
            'deckName': deck_name,
            'fields': note['fields'],
            'tags': note['tags'],
            'cards': note.get('cards', [])
        }
        
    print("\nSynchronizing database with Anki...")
    notes_to_add = []
    updated_count = 0
    skipped_count = 0
    
    for card in cards:
        # Construct tags
        tags = card.get("tags", [])
        tags.append(card['deck'].split("::")[-1].lower())
        tags = sorted(list(set(tags))) # unique and sorted tags

        model_name = card.get("model_name", "Engaging_Cloze_Model")
        if model_name == "Engaging_Speaking_Model":
            fields = {
                "Prompt": card.get("prompt", card.get("text", "")),
                "Scenario": card.get("scenario", ""),
                "Explanation": card.get("explanation", ""),
                "Usage_Examples": card.get("usage", ""),
                "Spanish_Translation": card.get("spanish", ""),
                "Audio": card.get("audio", ""),
                "Practice_Link": card.get("practice_link", card.get("practice_url", "")),
                "Recording_Hint": card.get("recording_hint", "Record yourself and compare your delivery with the model audio."),
            }
        else:
            fields = {
                "Text": card['text'],
                "Scenario": card['scenario'],
                "Explanation": card['explanation'],
                "Usage_Examples": card['usage'],
                "Spanish_Translation": card['spanish'],
                "Audio": card.get("audio", "")
            }
        
        # Text key normalized
        card_text_normalized = str(card.get('text') or card.get('prompt') or '').strip()
        
        if card_text_normalized in existing_anki_notes:
            # Note already exists. Check if we need to update deck, fields or tags
            existing = existing_anki_notes[card_text_normalized]
            note_id = existing['noteId']
            current_deck = existing['deckName']
            card_ids = existing['cards']
            
            # Check if deck needs to be updated (migrated)
            deck_updated = False
            if card['deck'] != current_deck:
                print(f"Migrating card {note_id} from deck '{current_deck}' to '{card['deck']}'...")
                invoke('changeDeck', cards=card_ids, deck=card['deck'])
                deck_updated = True
            
            # Compare fields
            fields_to_update = {}
            new_fields = fields
            
            for field_name, new_val in new_fields.items():
                existing_val = existing['fields'].get(field_name, {}).get('value', '')
                if existing_val != new_val:
                    fields_to_update[field_name] = new_val
            
            fields_updated = False
            if fields_to_update:
                invoke('updateNoteFields', note={"id": note_id, "fields": fields_to_update})
                fields_updated = True
                
            # Compare tags case-insensitively due to Anki's case-folding behavior
            existing_tags = sorted(list(set(existing['tags'])))
            existing_tags_lower = sorted(list(set(t.lower() for t in existing_tags)))
            tags_lower = sorted(list(set(t.lower() for t in tags)))
            tags_updated = False
            if tags_lower != existing_tags_lower:
                # Remove old tags
                if existing_tags:
                    invoke('removeTags', notes=[note_id], tags=" ".join(existing_tags))
                # Add new tags
                if tags:
                    invoke('addTags', notes=[note_id], tags=" ".join(tags))
                tags_updated = True
                
            if deck_updated or fields_updated or tags_updated:
                updated_count += 1
            else:
                skipped_count += 1
        else:
            # Note does not exist in Anki. Add to new notes list.
            note = {
                "deckName": card['deck'],
                "modelName": model_name,
                "fields": fields,
                "options": {
                    "allowDuplicate": False # Force unique note check in Anki
                },
                "tags": tags
            }
            notes_to_add.append(note)
            
    created_count = 0
    if notes_to_add:
        print(f"Uploading {len(notes_to_add)} new cards to Anki...")
        try:
            result = invoke('addNotes', notes=notes_to_add)
            created_count = len([r for r in result if r is not None])
        except Exception as e:
            print("[!] Bulk upload encountered an issue. Falling back to individual card uploads for safety...")
            for idx, note in enumerate(notes_to_add):
                try:
                    res = invoke('addNote', note=note)
                    if res:
                        created_count += 1
                except Exception as ex:
                    err_msg = str(ex)
                    if "duplicate" not in err_msg.lower():
                        print(f"    [-] Failed to import card '{note['fields']['Scenario']}': {err_msg}")
        
    print(f"\nSync summary: {created_count} cards created, {updated_count} cards updated, {skipped_count} cards skipped (already in sync).")

if __name__ == "__main__":
    import_database()
