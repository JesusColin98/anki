import json, urllib.request

LEGACY_ROOTS = [
    "AI_Learning_Path",
    "Books_Path",
    "Chinese",
    "English",
    "French",
    "German",
    "Italian",
    "Japanese",
    "Korean",
    "Networking_Security",
    "Philosophy",
    "Portuguese",
    "Russian",
    "Social_Skills",
    "SoftSkills",
    "Spanish",
    "Tech_Map_2026",
]

def anki(action, **params):
    req = urllib.request.Request('http://localhost:8765',
        data=json.dumps({'action': action, 'version': 6, 'params': params}).encode(),
        headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read())['result']

all_decks = anki('deckNames')

# Find all decks that start with a legacy root
to_delete = []
for deck in all_decks:
    for root in LEGACY_ROOTS:
        if deck == root or deck.startswith(root + '::'):
            to_delete.append(deck)
            break

print(f"Decks to delete: {len(to_delete)}")
for d in sorted(to_delete):
    print(f"  {d}")

# Delete them — cardsToo=False because they are all confirmed empty
result = anki('deleteDecks', decks=to_delete, cardsToo=False)
print(f"\nDeleted {len(to_delete)} legacy decks. Result: {result}")
