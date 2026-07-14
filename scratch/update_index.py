import json
import os

root = r"c:\Users\jesus\anki"
index_path = os.path.join(root, 'decks', 'index.json')

with open(index_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_entries = [
    {'deck': '03_Languages::English::06_Leadership_and_Executive_English::Executive_Updates::Executive_Updates', 'path': 'decks/03_Languages/English/06_Leadership_and_Executive_English/Executive_Updates/Executive_Updates.json', 'cards_count': 6},
    {'deck': '03_Languages::English::06_Leadership_and_Executive_English::Coaching_and_Performance::Coaching_and_Performance', 'path': 'decks/03_Languages/English/06_Leadership_and_Executive_English/Coaching_and_Performance/Coaching_and_Performance.json', 'cards_count': 5},
    {'deck': '03_Languages::English::07_English_for_Support_and_Ops::Incident_Communication::Incident_Communication', 'path': 'decks/03_Languages/English/07_English_for_Support_and_Ops/Incident_Communication/Incident_Communication.json', 'cards_count': 5},
    {'deck': '03_Languages::English::Phonetics::Connected_Speech_Advanced::Connected_Speech_Advanced', 'path': 'decks/03_Languages/English/Phonetics/Connected_Speech_Advanced/Connected_Speech_Advanced.json', 'cards_count': 5},
    {'deck': '02_AI_and_Data_Science::05_MLOps_and_LLMOps::01_Deployment_and_Observability::01_Deployment_and_Observability', 'path': 'decks/02_AI_and_Data_Science/05_MLOps_and_LLMOps/01_Deployment_and_Observability/01_Deployment_and_Observability.json', 'cards_count': 5},
    {'deck': '02_AI_and_Data_Science::06_Responsible_AI::01_Governance_and_Risk::01_Governance_and_Risk', 'path': 'decks/02_AI_and_Data_Science/06_Responsible_AI/01_Governance_and_Risk/01_Governance_and_Risk.json', 'cards_count': 4},
    {'deck': '02_AI_and_Data_Science::07_AI_Product_and_Strategy::01_AI_Product_Adoption::01_AI_Product_Adoption', 'path': 'decks/02_AI_and_Data_Science/07_AI_Product_and_Strategy/01_AI_Product_Adoption/01_AI_Product_Adoption.json', 'cards_count': 4},
    {'deck': '05_Soft_Skills_and_Leadership::Leadership::01_Delegation_and_Coaching::01_Delegation_and_Coaching', 'path': 'decks/05_Soft_Skills_and_Leadership/Leadership/01_Delegation_and_Coaching/01_Delegation_and_Coaching.json', 'cards_count': 3},
    {'deck': '05_Soft_Skills_and_Leadership::Leadership::02_Performance_and_Accountability::02_Performance_and_Accountability', 'path': 'decks/05_Soft_Skills_and_Leadership/Leadership/02_Performance_and_Accountability/02_Performance_and_Accountability.json', 'cards_count': 3},
    {'deck': '05_Soft_Skills_and_Leadership::Service_Leadership::01_Incident_and_Customer_Recovery::01_Incident_and_Customer_Recovery', 'path': 'decks/05_Soft_Skills_and_Leadership/Service_Leadership/01_Incident_and_Customer_Recovery/01_Incident_and_Customer_Recovery.json', 'cards_count': 3},
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

print('Updated index and validated JSON files.')
