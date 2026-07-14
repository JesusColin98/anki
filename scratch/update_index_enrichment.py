import json
import os

root = r"c:\Users\jesus\anki"
index_path = os.path.join(root, 'decks', 'index.json')

with open(index_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_entries = [
    {'deck': '03_Languages::English::01_Daily_Life::Colloquial_Cafe_and_Menu', 'path': 'decks/03_Languages/English/01_Daily_Life/Colloquial_Cafe_and_Menu.json', 'cards_count': 8},
    {'deck': '03_Languages::English::01_Daily_Life::Travel_and_Transport', 'path': 'decks/03_Languages/English/01_Daily_Life/Travel_and_Transport.json', 'cards_count': 8},
    {'deck': '03_Languages::English::03_Socializing::Everyday_Conversation', 'path': 'decks/03_Languages/English/03_Socializing/Everyday_Conversation.json', 'cards_count': 8},
    {'deck': '03_Languages::English::03_Socializing::Idioms_and_Jokes', 'path': 'decks/03_Languages/English/03_Socializing/Idioms_and_Jokes.json', 'cards_count': 8},
    {'deck': '03_Languages::English::Phonetics::Colloquial_Pronunciation_Patterns', 'path': 'decks/03_Languages/English/Phonetics/Colloquial_Pronunciation_Patterns.json', 'cards_count': 8},
]

existing_paths = {entry['path'] for entry in data['decks']}
for entry in new_entries:
    if entry['path'] not in existing_paths:
        data['decks'].append(entry)

data['total_cards'] = data.get('total_cards', 0) + sum(entry['cards_count'] for entry in new_entries if entry['path'] not in existing_paths)
data['total_decks'] = len(data['decks'])

with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

for entry in new_entries:
    path = os.path.join(root, entry['path'])
    with open(path, 'r', encoding='utf-8') as f:
        json.load(f)

print('Updated index with new English colloquial content and validated JSON files.')
