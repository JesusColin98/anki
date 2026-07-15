#!/usr/bin/env python3
"""Centralized Anki ADK Hub.

Provides a unified command-line interface for:
1. Syncing decks to Anki Desktop.
2. Validating deck folder structure and card syntax.
3. Cleaning up duplicate notes in Anki.
4. Auditing empty decks in Anki.
5. Deleting legacy empty decks.
6. Scraping web URLs and auto-generating cards via Gemini.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Any

# Root setup
BASE_DIR = Path(__file__).parent.resolve()
DECKS_DIR = BASE_DIR / "decks"
INDEX_FILE = DECKS_DIR / "index.json"

# Valid Pillars
VALID_PILLARS = {
    "01_Cloud_and_Infrastructure",
    "02_AI_and_Data_Science",
    "03_Languages",
    "04_Social_and_Humanities",
    "05_Soft_Skills_and_Leadership",
    "06_Business_and_Productivity",
}

# Import local modules
sys.path.insert(0, str(BASE_DIR))
from card_validator import sanitize_and_validate_card
from gemini_provider import generate_anki_cards_gemini
from scraper_agent import scrape_article, save_cards_to_deck
from adk_orchestrator import chunk_text
from anki_db_importer import get_learning_path_deck

def anki_invoke(action: str, **params) -> Any:
    """Helper to communicate with AnkiConnect."""
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
        print("[-] Error: Connecting to AnkiConnect failed. Is Anki Desktop running?", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        raise e

# -----------------
# COMMAND: VALIDATE
# -----------------
def cmd_validate() -> bool:
    """Validates that all decks conform to the 4-level deep structure and card syntax rules."""
    print("=== DECK HIERARCHY & CARD SYNTAX VALIDATION ===")
    if not INDEX_FILE.exists():
        print(f"[-] Error: index.json not found at {INDEX_FILE}", file=sys.stderr)
        return False

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []
    total_cards = 0

    for entry in data["decks"]:
        deck_name = entry["deck"]
        parts = deck_name.split("::")

        # 1. Level depth check
        if len(parts) != 4:
            errors.append(f"Deck '{deck_name}' does not have exactly 4 levels (has {len(parts)}).")
            continue

        # 2. Pillar validation
        if parts[0] not in VALID_PILLARS:
            errors.append(f"Deck '{deck_name}' has invalid pillar '{parts[0]}'.")

        # 3. File existence check
        file_path = BASE_DIR / entry["path"]
        if not file_path.exists():
            errors.append(f"Missing deck file: {file_path}")
            continue

        # 4. Card validation
        with open(file_path, "r", encoding="utf-8") as f:
            cards = json.load(f)

        for i, card in enumerate(cards):
            total_cards += 1
            is_valid, _, card_errors = sanitize_and_validate_card(card)
            if not is_valid:
                errors.append(f"Card {i} in '{deck_name}' failed validation: {card_errors}")

    print(f"Total Decks Validated: {len(data['decks'])}")
    print(f"Total Cards Validated: {total_cards}")

    if errors:
        print(f"\n[!] Found {len(errors)} validation errors:")
        for err in errors[:10]:
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors.")
        return False
    else:
        print(f"\n[OK] All {len(data['decks'])} decks and {total_cards} cards passed validation cleanly!")
        return True

# -------------
# COMMAND: SYNC
# -------------
def cmd_sync():
    """Runs 2-way synchronization with Anki Desktop."""
    print("=== SYNCHRONIZING DECKS WITH ANKI DESKTOP ===")
    
    # 1. Load and compile cards using anki_db_importer load_all_cards
    from anki_db_importer import load_all_cards
    cards = load_all_cards(base_dir=BASE_DIR)
    
    # 2. De-duplicate cards
    unique_cards = []
    seen_db_keys = set()
    for card in cards:
        m_name = card.get("model_name", "Engaging_Cloze_Model")
        t_key = card.get('prompt') if m_name == "Engaging_Speaking_Model" else card.get('text')
        if not t_key:
            t_key = card.get('text') or card.get('prompt') or ''
        key = (card['deck'], str(t_key).strip())
        
        if key not in seen_db_keys:
            seen_db_keys.add(key)
            unique_cards.append(card)
        else:
            print(f"[-] Warning: Ignored duplicate card in JSON database: Deck '{card['deck']}', Text '{t_key[:60]}...'")
    cards = unique_cards

    # 3. Ensure models exist
    models = anki_invoke('modelNames')
    for m_name in ["Engaging_Cloze_Model", "Engaging_Speaking_Model"]:
        if m_name not in models:
            print(f"[+] Creating custom model '{m_name}'...")
            from anki_db_importer import ensure_model_exists
            ensure_model_exists()
            break

    # 4. Ensure decks exist in Anki
    decks = set(card['deck'] for card in cards)
    for deck in sorted(decks):
        anki_invoke('createDeck', deck=deck)

    # 5. Fetch existing notes in Anki
    print("Fetching existing notes from Anki...")
    existing_note_ids = anki_invoke('findNotes', query='note:Engaging_Cloze_Model')
    try:
        speaking_ids = anki_invoke('findNotes', query='note:Engaging_Speaking_Model')
        existing_note_ids.extend(speaking_ids)
    except Exception:
        pass
    
    existing_notes_details = []
    batch_size = 500
    for i in range(0, len(existing_note_ids), batch_size):
        batch = existing_note_ids[i:i+batch_size]
        details = anki_invoke('notesInfo', notes=batch)
        existing_notes_details.extend(details)
        
    card_ids = []
    for note in existing_notes_details:
        if note.get('cards'):
            card_ids.append(note['cards'][0])
            
    card_details = []
    for i in range(0, len(card_ids), batch_size):
        batch = card_ids[i:i+batch_size]
        details = anki_invoke('cardsInfo', cards=batch)
        card_details.extend(details)
        
    note_to_deck = {card['note']: card['deckName'] for card in card_details}
    
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

    # 6. Synchronize
    notes_to_add = []
    updated_count = 0
    skipped_count = 0
    deck_migrations = {}
    
    for card in cards:
        # Construct tags using original tags if available
        tags = card.get("original_tags", card.get("tags", []))
        tags.append(card['deck'].split("::")[-1].lower())
        tags = sorted(list(set(tags)))
        
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
            card_text_normalized = str(card.get('prompt') or card.get('text') or '').strip()
        else:
            fields = {
                "Text": card['text'],
                "Scenario": card['scenario'],
                "Explanation": card['explanation'] + related_tags_html,
                "Usage_Examples": card['usage'],
                "Spanish_Translation": card['spanish'],
                "Audio": card.get("audio", "")
            }
            card_text_normalized = str(card.get('text') or card.get('prompt') or '').strip()
        
        if card_text_normalized in existing_anki_notes:
            existing = existing_anki_notes[card_text_normalized]
            note_id = existing['noteId']
            current_deck = existing['deckName']
            c_ids = existing['cards']
            
            deck_updated = False
            if card['deck'] != current_deck:
                deck_migrations.setdefault(card['deck'], []).extend(c_ids)
                deck_updated = True
            
            fields_to_update = {}
            for field_name, new_val in fields.items():
                existing_val = existing['fields'].get(field_name, {}).get('value', '')
                if existing_val != new_val:
                    fields_to_update[field_name] = new_val
            
            fields_updated = False
            if fields_to_update:
                anki_invoke('updateNoteFields', note={"id": note_id, "fields": fields_to_update})
                fields_updated = True
                
            existing_tags = sorted(list(set(existing['tags'])))
            existing_tags_lower = sorted(list(set(t.lower() for t in existing_tags)))
            tags_lower = sorted(list(set(t.lower() for t in tags)))
            tags_updated = False
            if tags_lower != existing_tags_lower:
                if existing_tags:
                    anki_invoke('removeTags', notes=[note_id], tags=" ".join(existing_tags))
                if tags:
                    anki_invoke('addTags', notes=[note_id], tags=" ".join(tags))
                tags_updated = True
                
            if deck_updated or fields_updated or tags_updated:
                updated_count += 1
            else:
                skipped_count += 1
        else:
            note = {
                "deckName": card['deck'],
                "modelName": model_name,
                "fields": fields,
                "options": {"allowDuplicate": False},
                "tags": tags
            }
            notes_to_add.append(note)
            
    if deck_migrations:
        print(f"\n[+] Processing {len(deck_migrations)} deck migrations in batch...")
        for target_deck, c_ids in deck_migrations.items():
            print(f"    [-] Migrating {len(c_ids)} cards to deck '{target_deck}'...")
            anki_invoke('changeDeck', cards=c_ids, deck=target_deck)
            
    created_count = 0
    if notes_to_add:
        print(f"Uploading {len(notes_to_add)} new cards to Anki in chunked batches...")
        batch_size = 100
        for i in range(0, len(notes_to_add), batch_size):
            batch = notes_to_add[i:i+batch_size]
            try:
                result = anki_invoke('addNotes', notes=batch)
                if result:
                    created_count += len([r for r in result if r is not None])
            except Exception as e:
                print(f"[!] Batch {i//batch_size + 1} encountered an issue. Falling back to individual card uploads for this batch...")
                for note in batch:
                    try:
                        res = anki_invoke('addNote', note=note)
                        if res:
                            created_count += 1
                    except Exception as ex:
                        err_msg = str(ex)
                        if "duplicate" not in err_msg.lower():
                            scenario_clean = note['fields']['Scenario'].encode('ascii', 'ignore').decode('ascii')
                            err_clean = err_msg.encode('ascii', 'ignore').decode('ascii')
                            print(f"    [-] Failed to import card '{scenario_clean}': {err_clean}")
                            
    print(f"\nSync summary: {created_count} cards created, {updated_count} cards updated, {skipped_count} cards skipped.")

# --------------
# COMMAND: CLEAN
# --------------
def cmd_clean():
    """Finds and deletes duplicate notes of model Engaging_Cloze_Model in Anki Connect."""
    print("=== CLEANING DUPLICATE NOTES IN ANKI ===")
    from clean_anki_duplicates import clean_duplicates
    clean_duplicates()

# --------------
# COMMAND: AUDIT
# --------------
def cmd_audit():
    """Identifies decks with zero notes (including subdecks) in Anki."""
    print("=== AUDITING EMPTY DECKS IN ANKI ===")
    all_decks = sorted(anki_invoke('deckNames'))
    empty_decks = []
    for deck in all_decks:
        if deck == 'Default':
            continue
        count = len(anki_invoke('findNotes', query=f'deck:"{deck}"'))
        if count == 0:
            empty_decks.append(deck)

    print(f"Decks with 0 notes (including sub-decks): {len(empty_decks)}")
    for d in empty_decks:
        print(f"  {d}")

# --------------------
# COMMAND: DELETE-LEGACY
# --------------------
def cmd_delete_legacy():
    """Deletes empty decks under the 6 pillars from Anki Desktop."""
    print("=== PURGING EMPTY DECKS IN ANKI ===")
    all_decks = sorted(anki_invoke('deckNames'))
    to_delete = []
    
    for deck in all_decks:
        if deck == 'Default':
            continue
        count = len(anki_invoke('findNotes', query=f'deck:"{deck}"'))
        if count == 0:
            to_delete.append(deck)

    print(f"Decks to delete (with 0 notes): {len(to_delete)}")
    for d in sorted(to_delete):
        print(f"  {d}")

    if to_delete:
        # Delete in descending order of length to delete children first
        to_delete_sorted = sorted(to_delete, key=len, reverse=True)
        result = anki_invoke('deleteDecks', decks=to_delete_sorted, cardsToo=True)
        print(f"Deleted {len(to_delete)} empty decks. Result: {result}")
    else:
        print("No empty decks to delete.")

# ----------------------
# COMMAND: SCRAPE-INGEST
# ----------------------
def cmd_scrape_ingest(url: str, deck_name: str):
    """Scrapes a URL, processes it via Map-Reduce chunking, calls Gemini API, and saves cards."""
    print(f"=== SCRAPE & INGEST: {url} -> {deck_name} ===")
    
    # 1. Scrape Web content
    article = scrape_article(url)
    full_text = article["full_text"]
    title = article["title"]
    
    print(f"[+] Scraped '{title}'. Splitting into rolling chunks...")
    chunks = chunk_text(full_text)
    
    total_cards = []
    for i, chunk in enumerate(chunks, start=1):
        print(f"  [->] Processing chunk {i}/{len(chunks)} with Gemini...")
        # Get generated cards from Gemini LLM
        chunk_cards = generate_anki_cards_gemini(chunk, deck_name)
        
        # Validate and sanitize each generated card
        validated_chunk_cards = []
        for card in chunk_cards:
            is_valid, cleaned_card, errs = sanitize_and_validate_card(card)
            if is_valid:
                validated_chunk_cards.append(cleaned_card)
            else:
                print(f"    [!] Card validation failed (Skipped): {errs}")
                
        total_cards.extend(validated_chunk_cards)
        
    print(f"[+] Total validated cards generated: {len(total_cards)}")
    
    if total_cards:
        # Save to deck file
        save_cards_to_deck(total_cards, deck_name)
        # Re-run index regeneration
        regenerate_index()
        print(f"[OK] Ingestion complete! Saved {len(total_cards)} cards to deck '{deck_name}'.")
    else:
        print("[-] Warning: No valid cards were generated.")

def regenerate_index():
    """Scans decks directory and regenerates index.json."""
    index_entries = []
    total_cards_count = 0
    
    for p in DECKS_DIR.glob("**/*.json"):
        if p.name == "index.json":
            continue
        try:
            with open(p, "r", encoding="utf-8") as f:
                cards = json.load(f)
            deck_name = str(p.relative_to(DECKS_DIR).with_suffix("")).replace("/", "::")
            index_entries.append({
                "deck": deck_name,
                "path": f"decks/{p.relative_to(DECKS_DIR).as_posix()}",
                "cards_count": len(cards)
            })
            total_cards_count += len(cards)
        except Exception as e:
            print(f"[-] Error indexing {p}: {e}")

    index_entries = sorted(index_entries, key=lambda x: x["deck"])
    
    new_index_data = {
        "total_cards": total_cards_count,
        "total_decks": len(index_entries),
        "decks": index_entries
    }
    
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(new_index_data, f, indent=2, ensure_ascii=False)
    print(f"[+] Regenerated index.json (Total cards: {total_cards_count}, Decks: {len(index_entries)})")

# ----
# MAIN
# ----
def main():
    parser = argparse.ArgumentParser(description="Centralized Anki ADK Operations Hub")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # validate
    subparsers.add_parser("validate", help="Validate deck structure and card syntax")
    
    # sync
    subparsers.add_parser("sync", help="Sync all deck JSON files to Anki Connect Desktop")
    
    # clean
    subparsers.add_parser("clean", help="Remove duplicate notes in Anki Connect")
    
    # audit
    subparsers.add_parser("audit", help="Audit empty decks in Anki")
    
    # delete-legacy
    subparsers.add_parser("delete-legacy", help="Delete empty legacy decks in Anki")
    
    # scrape-ingest
    scrape_parser = subparsers.add_parser("scrape-ingest", help="Scrape a URL and generate Anki cards using Gemini")
    scrape_parser.add_argument("url", help="Web article or doc URL to scrape")
    scrape_parser.add_argument("deck", help="Target deck (e.g. 03_Languages::English::News::General)")

    args = parser.parse_args()

    if args.command == "validate":
        success = cmd_validate()
        sys.exit(0 if success else 1)
    elif args.command == "sync":
        cmd_sync()
    elif args.command == "clean":
        cmd_clean()
    elif args.command == "audit":
        cmd_audit()
    elif args.command == "delete-legacy":
        cmd_delete_legacy()
    elif args.command == "scrape-ingest":
        cmd_scrape_ingest(args.url, args.deck)

if __name__ == "__main__":
    main()
