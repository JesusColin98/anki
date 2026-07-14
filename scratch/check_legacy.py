import json, urllib.request

def anki(action, **params):
    req = urllib.request.Request('http://localhost:8765',
        data=json.dumps({'action': action, 'version': 6, 'params': params}).encode(),
        headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read())['result']

LEGACY_ROOTS = [
    "AI_Learning_Path", "Books_Path", "Chinese", "English", "French", "German",
    "Italian", "Japanese", "Korean", "Networking_Security", "Philosophy",
    "Portuguese", "Russian", "Social_Skills", "SoftSkills", "Spanish", "Tech_Map_2026"
]

all_decks = anki('deckNames')
legacy_decks = []
for deck in all_decks:
    for root in LEGACY_ROOTS:
        if deck == root or deck.startswith(root + "::"):
            legacy_decks.append(deck)
            break

print("Legacy decks and their card counts:")
total_cards = 0
for d in sorted(legacy_decks):
    cards = anki('findNotes', query=f'deck:"{d}"')
    if len(cards) > 0:
        print(f"  {d}: {len(cards)} cards")
        total_cards += len(cards)
    else:
        print(f"  {d}: 0 cards")

print(f"Total cards in all legacy decks: {total_cards}")
