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
:root {
    --bg-color: #fafafa;
    --card-bg: #ffffff;
    --text-color: #1a1a1a;
    --text-dark: #111111;
    --border-color: #e5e5e5;
    --cloze-color: #2563eb;
    --cloze-bg: #eff6ff;
    --cloze-border: #bfdbfe;
    --badge-color: #8c8c8c;
    --badge-bg: #f5f5f5;
    --explanation-border: #3b82f6;
    --examples-border: #10b981;
    --tab-active-bg: #f1f5f9;
    --tab-active-border: #3b82f6;
    --success-color: #10b981;
    --success-bg: #ecfdf5;
    --mismatch-color: #ef4444;
    --mismatch-bg: #fef2f2;
}

.nightMode {
    --bg-color: #0f172a;
    --card-bg: #1e293b;
    --text-color: #e2e8f0;
    --text-dark: #f8fafc;
    --border-color: #334155;
    --cloze-color: #60a5fa;
    --cloze-bg: #1e3a8a;
    --cloze-border: #2563eb;
    --badge-color: #94a3b8;
    --badge-bg: #334155;
    --explanation-border: #60a5fa;
    --examples-border: #34d399;
    --tab-active-bg: #334155;
    --tab-active-border: #60a5fa;
    --success-color: #34d399;
    --success-bg: #065f46;
    --mismatch-color: #f87171;
    --mismatch-bg: #7f1d1d;
}

.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 19px;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--bg-color);
    padding: 24px;
    max-width: 650px;
    margin: 0 auto;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}

.cloze {
    font-weight: bold;
    color: var(--cloze-color);
    background-color: var(--cloze-bg);
    padding: 2px 8px;
    border-radius: 6px;
    border-bottom: 2px dashed var(--cloze-border);
}

.scenario-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--badge-color);
    background-color: var(--badge-bg);
    padding: 4px 12px;
    border-radius: 9999px;
    margin-bottom: 16px;
}

hr {
    border: none;
    border-top: 1px solid var(--border-color);
    margin: 20px 0;
}

.sentence-front {
    font-size: 22px;
    font-weight: 500;
    color: var(--text-dark);
    margin: 12px 0;
}

.explanation-section {
    background-color: var(--card-bg);
    border-left: 4px solid var(--explanation-border);
    border: 1px solid var(--border-color);
    border-left-width: 4px;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 16px;
    text-align: left;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.explanation-section h3 {
    margin: 0 0 6px 0;
    font-size: 13px;
    color: var(--explanation-border);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.examples-section {
    background-color: var(--card-bg);
    border-left: 4px solid var(--examples-border);
    border: 1px solid var(--border-color);
    border-left-width: 4px;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 16px;
    text-align: left;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.examples-section h3 {
    margin: 0 0 6px 0;
    font-size: 13px;
    color: var(--examples-border);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.examples-section ul {
    margin: 0;
    padding-left: 20px;
    color: var(--text-color);
}

.examples-section li {
    margin-bottom: 6px;
}

.examples-section code {
    background-color: var(--badge-bg);
    color: var(--text-dark);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 14px;
}

details {
    background-color: var(--badge-bg);
    padding: 10px 14px;
    border-radius: 8px;
    margin-top: 16px;
    font-size: 15px;
    color: var(--text-color);
    cursor: pointer;
    text-align: left;
    transition: background-color 0.2s;
    border: 1px solid var(--border-color);
}

details:hover {
    background-color: var(--border-color);
}

details summary {
    font-weight: 600;
    outline: none;
    user-select: none;
}

details p {
    margin: 8px 0 0 0;
    color: var(--text-color);
}

/* Tabs Styling */
.tabs-container {
    margin: 16px 0;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--card-bg);
    overflow: hidden;
}
.tabs-header {
    display: flex;
    background: var(--badge-bg);
    border-bottom: 1px solid var(--border-color);
}
.tab-btn {
    flex: 1;
    background: transparent;
    border: none;
    padding: 10px;
    font-size: 14px;
    font-weight: 500;
    color: var(--badge-color);
    cursor: pointer;
    transition: all 0.2s;
    outline: none;
}
.tab-btn:hover {
    color: var(--text-color);
}
.tab-btn.active {
    background: var(--card-bg);
    color: var(--cloze-color);
    border-bottom: 2px solid var(--tab-active-border);
}
.tab-content {
    display: none;
    padding: 16px;
    text-align: left;
}
.tab-content.active {
    display: block;
}

/* Match Game Styling */
.match-game {
    display: flex;
    gap: 16px;
    margin: 20px 0;
    text-align: left;
}
.match-game .column {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.match-game h4 {
    margin: 0 0 8px 0;
    font-size: 14px;
    color: var(--badge-color);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.mg-item {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 10px 12px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    user-select: none;
}
.mg-item:hover {
    border-color: var(--cloze-color);
    background: var(--tab-active-bg);
}
.mg-item.selected {
    border-color: var(--cloze-color);
    background: var(--cloze-bg);
    color: var(--cloze-color);
    font-weight: 600;
}
.mg-item.matched {
    cursor: default;
    opacity: 0.6;
}
.mg-item.matched.success {
    background: var(--success-bg);
    border-color: var(--success-color);
    color: var(--success-color);
    opacity: 0.8;
}
.mg-item.mismatch {
    background: var(--mismatch-bg);
    border-color: var(--mismatch-color);
    color: var(--mismatch-color);
}
.mg-success-banner {
    margin-top: 12px;
    padding: 8px;
    background: var(--success-bg);
    color: var(--success-color);
    border-radius: 6px;
    text-align: center;
    font-weight: 600;
    font-size: 14px;
}

/* Visual Cloze Diagrams (Mermaid SVG nodes) */
.mermaid .cloze-node rect,
.mermaid .cloze-node circle,
.mermaid .cloze-node polygon {
    fill: var(--badge-bg) !important;
    stroke: var(--border-color) !important;
    stroke-dasharray: 4 !important;
    cursor: pointer;
}
.mermaid .cloze-node text {
    fill: transparent !important;
}
.mermaid .cloze-node.revealed rect,
.mermaid .cloze-node.revealed circle,
.mermaid .cloze-node.revealed polygon {
    fill: var(--cloze-bg) !important;
    stroke: var(--cloze-color) !important;
    stroke-dasharray: none !important;
}
.mermaid .cloze-node.revealed text {
    fill: var(--cloze-color) !important;
}

/* Related Tags Section */
.related-tags-section {
    margin-top: 16px;
    font-size: 13px;
    color: var(--badge-color);
    border-top: 1px dashed var(--border-color);
    padding-top: 8px;
    text-align: left;
}
.search-tag-link {
    color: var(--cloze-color);
    text-decoration: none;
    margin-right: 8px;
    font-weight: 500;
}
.search-tag-link:hover {
    text-decoration: underline;
}
"""

    speaking_css = cloze_css + """
.prompt-block {
    font-size: 22px;
    font-weight: 600;
    color: var(--text-dark);
    margin-bottom: 16px;
}

.audio-player {
    background: var(--cloze-bg);
    border-left: 4px solid var(--cloze-color);
    padding: 12px 16px;
    border-radius: 8px;
    margin: 12px 0;
}

.practice-link {
    margin-top: 10px;
}

.practice-link a {
    color: var(--cloze-color);
    font-weight: 600;
    text-decoration: none;
}

.practice-link a:hover {
    text-decoration: underline;
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

def get_learning_path_deck(deck_name, card):
    # Route English language cards to 4 core Learning Paths
    dn = deck_name.lower()
    
    # Try to check if it has a source file or path to determine context
    source_file = card.get("source_file", "")
    sf = source_file.replace("\\", "/").lower()
    
    if "05_interviews" in sf or "interview" in dn or "leadership" in dn or "executive" in dn:
        return "03_Languages::English::Learning_Paths::03_Interview_and_Career"
    elif "02_workplace" in sf or "06_phone_calls" in sf or "professional" in dn or "support" in dn or "incident" in dn:
        return "03_Languages::English::Learning_Paths::02_Workplace_and_Service"
    elif "07_health" in sf or "08_education" in sf or "academic" in dn or "philosophical" in dn or "health" in dn:
        return "03_Languages::English::Learning_Paths::04_Academic_and_Health"
    else:
        # Default Daily & Social for daily, travel, social, socializing, A1, etc.
        return "03_Languages::English::Learning_Paths::01_Daily_and_Social"

def load_all_cards(base_dir="."):
    decks_dir = os.path.join(base_dir, "decks")
    raw_cards = []
    
    if os.path.exists(decks_dir):
        print(f"Reading cards from nested decks directory: {decks_dir}...")
        for root, _, files in os.walk(decks_dir):
            for file in sorted(files):
                if file.endswith(".json") and file != "index.json" and file != "manifest.json":
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            deck_cards = json.load(f)
                            rel_path = os.path.relpath(file_path, decks_dir)
                            derived_deck = str(Path(rel_path).with_suffix("")).replace(os.sep, "::")
                            for card in deck_cards:
                                if "deck" not in card or not card["deck"]:
                                    card["deck"] = derived_deck
                                raw_cards.append(card)
                    except Exception as e:
                        print(f"Warning: Could not load {file_path}: {e}", file=sys.stderr)
    else:
        monolith_file = os.path.join(base_dir, "anki_cards_database.json")
        if os.path.exists(monolith_file):
            print(f"Reading database {monolith_file}...")
            with open(monolith_file, "r", encoding="utf-8") as f:
                raw_cards = json.load(f)
        else:
            print("Error: Neither decks/ directory nor anki_cards_database.json found.", file=sys.stderr)
            sys.exit(1)

    # Compile the raw cards using template_engine and flatten decks
    from template_engine import build_card
    compiled_cards = []
    
    for card in raw_cards:
        # If it is already flat (legacy fallback), keep it as is
        if "content" not in card:
            # Flatten deck name to 3 levels
            deck_parts = card["deck"].split("::")
            if len(deck_parts) == 4:
                card["deck"] = "::".join(deck_parts[1:])
            # Natively route English cards into Learning Paths by default
            if card["deck"].startswith("03_Languages::English") and "::Phonetics" not in card["deck"]:
                card["deck"] = get_learning_path_deck(card["deck"], card)
            compiled_cards.append(card)
            continue
            
        # Reconstruct flat dictionary for build_card
        flat_data = {
            "deck": card.get("deck"),
            "id": card.get("id"),
            "template": card.get("template"),
            **card.get("metadata", {}),
            **card.get("content", {}),
            **card.get("mnemonics", {}),
            **card.get("interactivity", {})
        }
        
        try:
            compiled_nested = build_card(card["template"], flat_data)
            
            # Flatten compiled nested output in-memory for the sync engine
            compiled = {
                "id": compiled_nested.get("id"),
                "deck": compiled_nested.get("deck"),
                "template": compiled_nested.get("template"),
                **compiled_nested.get("metadata", {}),
                **compiled_nested.get("content", {}),
                **compiled_nested.get("mnemonics", {}),
                **compiled_nested.get("interactivity", {})
            }
            
            # Flatten deck name to 3 levels (omit Pillar part)
            deck_parts = compiled["deck"].split("::")
            if len(deck_parts) == 4:
                compiled["deck"] = "::".join(deck_parts[1:])
                
            # Natively route English cards into Learning Paths by default
            if compiled["deck"].startswith("03_Languages::English") and "::Phonetics" not in compiled["deck"]:
                compiled["deck"] = get_learning_path_deck(compiled["deck"], compiled)
                
            # Preserve original properties for model mapping & tag generation
            compiled["template"] = card["template"]
            compiled["original_tags"] = card.get("metadata", {}).get("tags", [])
            compiled["model_name"] = "Engaging_Speaking_Model" if card["template"] == "T12_SpeakingPractice" else "Engaging_Cloze_Model"
            
            compiled_cards.append(compiled)
        except Exception as e:
            print(f"Warning: Failed to compile card {card.get('id', 'unknown')}: {e}", file=sys.stderr)
            
    print(f"Compiled and loaded {len(compiled_cards)} total cards.")
    return compiled_cards

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
        
    # Query all existing notes of our custom models in Anki
    print("\nFetching existing notes from Anki...")
    existing_note_ids = invoke('findNotes', query='note:Engaging_Cloze_Model')
    try:
        speaking_ids = invoke('findNotes', query='note:Engaging_Speaking_Model')
        existing_note_ids.extend(speaking_ids)
    except Exception:
        pass
    
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
        
    # Create mapping of Text/Prompt -> (noteId, deckName, fields, tags, cards)
    existing_anki_notes = {}
    for note in existing_notes_details:
        note_id = note['noteId']
        deck_name = note_to_deck.get(note_id, "Unknown")
        text_val = note['fields'].get('Text', {}).get('value', '')
        if not text_val and 'Prompt' in note['fields']:
            text_val = note['fields'].get('Prompt', {}).get('value', '')
        text_val = text_val.strip()
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

        # Generate related search links (Option A)
        tags_list = card.get("original_tags", [])
        topic_tags = [t for t in tags_list if t.startswith("source::") or t in ["memory_techniques", "feynman_method", "peg_system", "mnemonic_palace", "phonetics", "connected_speech"]]
        related_tags_html = ""
        if topic_tags:
            links_html = " ".join(f'<a class="search-tag-link" href="anki://search?q=tag:{t}">#{t}</a>' for t in topic_tags)
            related_tags_html = f'<div class="related-tags-section"><b>Búsquedas Relacionadas:</b> {links_html}</div>'

        model_name = card.get("model_name", "Engaging_Cloze_Model")
        if model_name == "Engaging_Speaking_Model":
            fields = {
                "Prompt": card.get("prompt", card.get("text", "")),
                "Scenario": card.get("scenario", ""),
                "Explanation": card.get("explanation", "") + related_tags_html,
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
                "Explanation": card['explanation'] + related_tags_html,
                "Usage_Examples": card['usage'],
                "Spanish_Translation": card['spanish'],
                "Audio": card.get("audio", "")
            }
        
        # Text key normalized (align key mapping based on model type)
        if model_name == "Engaging_Speaking_Model":
            card_text_normalized = str(card.get('prompt') or card.get('text') or '').strip()
        else:
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
                        scenario_clean = note['fields']['Scenario'].encode('ascii', 'ignore').decode('ascii')
                        err_clean = err_msg.encode('ascii', 'ignore').decode('ascii')
                        print(f"    [-] Failed to import card '{scenario_clean}': {err_clean}")
        
    print(f"\nSync summary: {created_count} cards created, {updated_count} cards updated, {skipped_count} cards skipped (already in sync).")

if __name__ == "__main__":
    import_database()
