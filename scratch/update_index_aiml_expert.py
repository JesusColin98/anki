import json
import os
from pathlib import Path

root = Path(r"c:\Users\jesus\anki")
index_path = root / "decks" / "index.json"

with open(index_path, "r", encoding="utf-8") as f:
    data = json.load(f)

base_dir = root / "decks" / "02_AI_and_Data_Science" / "08_Advanced_AI_Engineering"
new_entries = []

for json_path in sorted(base_dir.rglob("*.json")):
    rel_path = json_path.relative_to(root).as_posix()
    with open(json_path, "r", encoding="utf-8") as f:
        cards = json.load(f)
    deck_name = cards[0]["deck"] if cards else ""
    new_entries.append({
        "deck": deck_name,
        "path": rel_path,
        "cards_count": len(cards),
    })

existing_paths = {entry["path"] for entry in data.get("decks", [])}
added = 0
for entry in new_entries:
    if entry["path"] not in existing_paths:
        data["decks"].append({
            "deck": entry["deck"],
            "path": entry["path"],
            "cards_count": entry["cards_count"],
        })
        existing_paths.add(entry["path"])
        added += 1

# Recompute totals
edata = data.get("decks", [])
# Recalculate from actual entries (more reliable than incremental counting)
data["total_cards"] = sum(int(entry.get("cards_count", 0)) for entry in edata)
data["total_decks"] = len(edata)

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Updated index with {added} new AI/ML expert decks and validated JSON files.")
