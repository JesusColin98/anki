import json
from pathlib import Path

root = Path(r"c:\Users\jesus\anki")
index_path = root / "decks" / "index.json"

with open(index_path, "r", encoding="utf-8") as f:
    data = json.load(f)

path = "decks/03_Languages/English/Phonetics/Shadowing_Dictation_and_Real_Conversation.json"
with open(root / path, "r", encoding="utf-8") as f:
    cards = json.load(f)

entry = {
    "deck": cards[0]["deck"],
    "path": path,
    "cards_count": len(cards),
}

existing_paths = {item["path"] for item in data.get("decks", [])}
if path not in existing_paths:
    data["decks"].append(entry)

data["total_cards"] = sum(int(item.get("cards_count", 0)) for item in data.get("decks", []))
data["total_decks"] = len(data.get("decks", []))

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Updated index with shadowing and dictation deck.")
