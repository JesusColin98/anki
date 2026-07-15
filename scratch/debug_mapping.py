import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
MANIFEST_PATH = BASE_DIR / "decks" / "03_Languages" / "English" / "Variant_Pipeline" / "manifest.json"

def invoke(action, **params):
    payload = {'action': action, 'version': 6}
    if params:
        payload['params'] = params
    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8765', data=req_data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        return res['result']

def debug():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    json_keys = set()
    pipeline_dir = MANIFEST_PATH.parent
    for sub in pipeline_dir.iterdir():
        if sub.is_dir():
            for json_file in sub.glob("*.json"):
                with open(json_file, "r", encoding="utf-8") as f:
                    cards = json.load(f)
                for card in cards:
                    text_key = str(card.get("text") or card.get("prompt") or "").strip()
                    json_keys.add(text_key)
                    
    print(f"Total unique keys in JSON files: {len(json_keys)}")
    
    note_ids = invoke('findNotes', query='note:Engaging_Cloze_Model')
    try:
        speaking_ids = invoke('findNotes', query='note:Engaging_Speaking_Model')
        note_ids.extend(speaking_ids)
    except Exception:
        pass
        
    notes = invoke('notesInfo', notes=note_ids)
    anki_keys = set()
    for note in notes:
        text_val = note['fields'].get('Text', {}).get('value', '')
        if not text_val and 'Prompt' in note['fields']:
            text_val = note['fields'].get('Prompt', {}).get('value', '')
        text_val = text_val.strip()
        anki_keys.add(text_val)
        
    print(f"Total unique keys in Anki: {len(anki_keys)}")
    
    intersect = json_keys.intersection(anki_keys)
    print(f"Intersection count: {len(intersect)}")
    
    missing = list(json_keys - anki_keys)[:10]
    print("Example missing from Anki:")
    for m in missing:
        print(f"  - {repr(m)}")

if __name__ == "__main__":
    debug()
