import json
from pathlib import Path

report = json.loads(Path('scratch/deep_audit_report.json').read_text(encoding='utf-8'))

print('=== BOILERPLATE REMAINING ===')
for r in report['per_file']:
    if r.get('issue_type_counts', {}).get('boilerplate_explanation', 0):
        for rec in r['issues']:
            for iss in rec['issues']:
                if iss['type'] == 'boilerplate_explanation':
                    print(f"File: {r['file']}")
                    print(f"Card: {rec['card_id']} | {rec['template']}")
                    print(f"Detail: {iss['detail']}")
                    print()

print('=== TRIVIAL CLOZE (all 16) ===')
for r in report['per_file']:
    if r.get('issue_type_counts', {}).get('trivial_cloze', 0):
        for rec in r['issues']:
            for iss in rec['issues']:
                if iss['type'] == 'trivial_cloze':
                    print(f"File: {r['file']} | Card: {rec['card_id']}")
                    print(f"  Text: {iss['detail']}")
