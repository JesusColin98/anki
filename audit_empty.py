import json, urllib.request

def anki(action, **params):
    req = urllib.request.Request('http://localhost:8765',
        data=json.dumps({'action': action, 'version': 6, 'params': params}).encode(),
        headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read())['result']

all_decks = sorted(anki('deckNames'))

empty_decks = []
for deck in all_decks:
    if deck == 'Default':
        continue
    count = len(anki('findNotes', query=f'deck:"{deck}"'))
    if count == 0:
        empty_decks.append(deck)

print(f'Decks with 0 notes (including sub-decks): {len(empty_decks)}')
for d in empty_decks:
    print(f'  {d}')
