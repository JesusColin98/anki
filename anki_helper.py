import json
import urllib.request
import urllib.error
import argparse
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
            if len(res) != 2:
                raise Exception('Response has an unexpected number of fields')
            if 'error' not in res:
                raise Exception('Response is missing required error field')
            if 'result' not in res:
                raise Exception('Response is missing required result field')
            if res['error'] is not None:
                raise Exception(res['error'])
            return res['result']
    except urllib.error.URLError as e:
        print(f"Error connecting to AnkiConnect. Is Anki running and the AnkiConnect add-on installed?", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def list_decks():
    print("Fetching Anki Decks...")
    try:
        decks = invoke('deckNames')
        print("\nAvailable Decks:")
        for deck in decks:
            print(f" - {deck}")
    except Exception as e:
        print(f"Failed to list decks: {e}", file=sys.stderr)

def create_card(deck, front, back):
    print(f"Creating a test card in deck '{deck}'...")
    
    # We first verify if the deck exists. If it doesn't, we can ask AnkiConnect to create it, or fail gracefully.
    try:
        decks = invoke('deckNames')
        if deck not in decks:
            print(f"Deck '{deck}' does not exist. Creating deck '{deck}'...")
            invoke('createDeck', deck=deck)
    except Exception as e:
        print(f"Failed to verify/create deck: {e}", file=sys.stderr)
        sys.exit(1)
        
    note = {
        'deckName': deck,
        'modelName': 'Basic',
        'fields': {
            'Front': front,
            'Back': back
        },
        'options': {
            'allowDuplicate': True
        },
        'tags': ['test']
    }
    
    try:
        note_id = invoke('addNote', note=note)
        print(f"Successfully created card! Note ID: {note_id}")
    except Exception as e:
        print(f"Failed to create card: {e}", file=sys.stderr)
        print("\nTip: Make sure you have a 'Basic' note type/model with 'Front' and 'Back' fields in Anki.", file=sys.stderr)

def delete_all_decks():
    print("Fetching decks to delete...")
    try:
        decks = invoke('deckNames')
        if not decks:
            print("No decks found.")
            return
        
        print(f"Decks to delete: {decks}")
        # Note: Anki Connect's deleteDecks will delete the specified decks.
        # If 'Default' is deleted, Anki automatically recreates an empty 'Default' deck.
        invoke('deleteDecks', decks=decks, cardsToo=True)
        print("Successfully deleted all decks.")
    except Exception as e:
        print(f"Failed to delete decks: {e}", file=sys.stderr)

def import_deck_from_url(url):
    import os
    print(f"Downloading deck from: {url} ...")
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    temp_file = os.path.join(temp_dir, 'downloaded_deck.apkg')
    
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    try:
        with urllib.request.urlopen(req) as response, open(temp_file, 'wb') as out_file:
            out_file.write(response.read())
        print(f"File downloaded to: {temp_file}")
        
        abs_path = os.path.abspath(temp_file)
        print("Importing into Anki via AnkiConnect...")
        invoke('importPackage', path=abs_path)
        print("Import successful! The deck has been loaded into Anki.")
        
        # Clean up
        os.remove(temp_file)
        try:
            os.rmdir(temp_dir)
        except OSError:
            pass
    except Exception as e:
        print(f"Failed to download or import deck: {e}", file=sys.stderr)
        if os.path.exists(temp_file):
            os.remove(temp_file)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Helper CLI for Anki Integration")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommand to run")
    
    # List command
    subparsers.add_parser("list", help="List all local Anki decks")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a card in Anki")
    create_parser.add_argument("--deck", default="Default", help="Target deck name (default: Default)")
    create_parser.add_argument("--front", default="Test Front Side", help="Front content of the card")
    create_parser.add_argument("--back", default="Test Back Side", help="Back content of the card")
    
    # Delete all command
    subparsers.add_parser("delete-all", help="Delete all decks (and their cards) in Anki")
    
    # Import command
    import_parser = subparsers.add_parser("import", help="Download and import a deck from a URL")
    import_parser.add_argument("url", help="URL of the .apkg file to download and import")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_decks()
    elif args.command == "create":
        create_card(args.deck, args.front, args.back)
    elif args.command == "delete-all":
        delete_all_decks()
    elif args.command == "import":
        import_deck_from_url(args.url)

if __name__ == "__main__":
    main()
