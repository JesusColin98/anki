import json
import os

langs = ['Chinese', 'French', 'German', 'Italian', 'Japanese', 'Korean', 'Portuguese', 'Russian', 'Spanish']
files_to_check = []
for lang in langs:
    base = f'decks/03_Languages/{lang}'
    for root, dirs, files in os.walk(base):
        for f in files:
            files_to_check.append(os.path.join(root, f))

# Also add the cloud/security files
files_to_check.extend([
    'decks/01_Cloud_and_Infrastructure/Cybersecurity/Defense_Evasion/03_Defense_Evasion.json',
    'decks/01_Cloud_and_Infrastructure/Cybersecurity/Reconnaissance/02_Reconnaissance.json',
    'decks/01_Cloud_and_Infrastructure/Networking/Fundamentals/01_Fundamentals.json'
])

print("Current counts in target JSON files:")
under_count = 0
for f in sorted(files_to_check):
    if os.path.exists(f):
        data = json.load(open(f, encoding='utf-8'))
        print(f"  {f}: {len(data)} cards")
        if len(data) < 20:
            under_count += 1
    else:
        print(f"  {f}: DOES NOT EXIST")

print(f"\nTotal files with less than 20 cards: {under_count}")
