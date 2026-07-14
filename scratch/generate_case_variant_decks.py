import json
from pathlib import Path

root = Path(r"C:\Users\jesus\anki")
index_path = root / "decks" / "index.json"
source_path = root / "decks" / "03_Languages" / "English" / "08_Real_Scenario_Expansion" / "05_Interviews_and_Careers" / "05_Interviews_and_Careers.json"

with open(index_path, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(source_path, "r", encoding="utf-8") as f:
    source_cards = json.load(f)

existing_paths = {item["path"] for item in data.get("decks", [])}

variant_specs = [
    ("01_Speaking", "Speak this out loud and record yourself.", "speaking"),
    ("02_Listening", "Complete the sentence you hear in context.", "listening"),
    ("03_Writing", "Write a short response using the same idea.", "writing"),
    ("04_Dialogue", "Complete the short dialogue naturally.", "dialogue"),
]

selected_cards = source_cards[:80]

all_cards = []
for card in selected_cards:
    base_text = card.get("text", "")
    base_spanish = card.get("spanish", "")
    base_scenario = card.get("scenario", "Scenario")
    for folder_name, instruction, variant_type in variant_specs:
        if variant_type == "speaking":
            text = f"Say this out loud: {base_text}"
            explanation = f"Practice pronunciation and fluency. Use the same meaning as the source item: {base_text}"
            usage = f"Record yourself for 10–15 seconds and keep the idea natural."
            spanish = f"Practica esta idea en voz alta: {base_spanish}"
        elif variant_type == "listening":
            text = f"Listen and complete the phrase: {base_text}"
            explanation = f"This is a listening reinforcement card derived from the same base scenario."
            usage = f"Focus on stress, linking, and the core meaning of the phrase."
            spanish = f"Escucha y completa la idea: {base_spanish}"
        elif variant_type == "writing":
            text = f"Write a short response using: {base_text}"
            explanation = f"This is a writing reinforcement card derived from the same base scenario."
            usage = f"Write 2–3 sentences that keep the same meaning and feel natural."
            spanish = f"Escribe una respuesta breve usando: {base_spanish}"
        else:
            text = f"Complete the dialogue: {base_text}"
            explanation = f"This is a dialogue reinforcement card derived from the same base scenario."
            usage = f"Use the phrase naturally and keep the exchange realistic."
            spanish = f"Completa el diálogo usando: {base_spanish}"

        all_cards.append({
            "deck": f"03_Languages::English::Case_Variants::{folder_name}",
            "text": text,
            "scenario": f"{base_scenario} · {variant_type.title()}",
            "explanation": explanation,
            "usage": usage,
            "spanish": spanish,
            "tags": ["english", "case_variant", variant_type, "deterministic"],
            "source_text": base_text,
            "source_spanish": base_spanish,
            "variant_type": variant_type,
        })

for folder_name, _, _ in variant_specs:
    out_path = root / "decks" / "03_Languages" / "English" / "Case_Variants" / folder_name / f"{folder_name}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    subset = [c for c in all_cards if c["deck"].endswith(folder_name)]
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(subset, f, indent=2, ensure_ascii=False)
        f.write("\n")
    rel_path = out_path.relative_to(root).as_posix()
    if rel_path not in existing_paths:
        data["decks"].append({
            "deck": f"03_Languages::English::Case_Variants::{folder_name}",
            "path": rel_path,
            "cards_count": len(subset),
        })
        existing_paths.add(rel_path)

data["total_cards"] = sum(int(entry.get("cards_count", 0)) for entry in data.get("decks", []))
data["total_decks"] = len(data.get("decks", []))
with open(index_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Created {len(all_cards)} deterministic case-variant cards across {len(variant_specs)} variants.")
