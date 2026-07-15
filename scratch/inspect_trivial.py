import json, sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

report = json.loads(Path('scratch/deep_audit_report.json').read_text(encoding='utf-8'))

print('=== ALL TRIVIAL CLOZE ===')
for r in report['per_file']:
    if r.get('issue_type_counts', {}).get('trivial_cloze', 0):
        for rec in r['issues']:
            for iss in rec['issues']:
                if iss['type'] == 'trivial_cloze':
                    detail = iss['detail'].encode('ascii', errors='replace').decode('ascii')
                    print(f"File: {r['file']}")
                    print(f"  Card: {rec['card_id']} | {rec['template']}")
                    print(f"  Text: {detail}")
                    print()
