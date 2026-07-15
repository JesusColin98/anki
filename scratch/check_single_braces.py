import urllib.request
import json

def run():
    # Query notes containing '{c1::'
    query = '"{c1::"'
    payload = {'action': 'findNotes', 'version': 6, 'params': {'query': query}}
    req = urllib.request.Request('http://127.0.0.1:8765', data=json.dumps(payload).encode('utf-8'))
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            notes = res.get('result', [])
            print(f"Notes in Anki containing '{{c1::' (single brace): {len(notes)}")
            
            # Fetch details of first few
            if notes:
                details_payload = {'action': 'notesInfo', 'version': 6, 'params': {'notes': notes[:5]}}
                req2 = urllib.request.Request('http://127.0.0.1:8765', data=json.dumps(details_payload).encode('utf-8'))
                with urllib.request.urlopen(req2) as resp2:
                    details = json.loads(resp2.read().decode('utf-8'))['result']
                    for n in details:
                        text_val = n['fields'].get('Text', {}).get('value', '').encode('ascii', 'ignore').decode('ascii')
                        print(f"  Note ID {n['noteId']}: {text_val[:100]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
