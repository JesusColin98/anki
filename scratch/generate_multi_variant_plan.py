import json
from pathlib import Path
from collections import defaultdict

root = Path(r"C:\Users\jesus\anki")
source_dir = root / "decks" / "03_Languages" / "English" / "08_Real_Scenario_Expansion"
output_dir = root / "decks" / "03_Languages" / "English" / "Variant_Pipeline"
output_dir.mkdir(parents=True, exist_ok=True)

source_files = [
    source_dir / "05_Interviews_and_Careers" / "05_Interviews_and_Careers.json",
    source_dir / "06_Phone_Calls_and_Customer_Service" / "06_Phone_Calls_and_Customer_Service.json",
    source_dir / "07_Health_and_Emergencies" / "07_Health_and_Emergencies.json",
    source_dir / "08_Education_and_Academic_Contexts" / "08_Education_and_Academic_Contexts.json",
]

variant_specs = [
    ("speaking", "Say this out loud and record yourself.", "Practica esta idea en voz alta."),
    ("listening", "Listen and complete the phrase in context.", "Escucha y completa la idea."),
    ("writing", "Write a short response using the same idea.", "Escribe una respuesta corta usando la misma idea."),
    ("dialogue", "Complete the dialogue naturally.", "Completa el diálogo de forma natural."),
]

all_cards = []
for source_file in source_files:
    with open(source_file, "r", encoding="utf-8") as f:
        cards = json.load(f)
    for card in cards[:20]:
        base_text = card.get("text", "")
        base_scenario = card.get("scenario", "Scenario")
        base_spanish = card.get("spanish", "")
        for variant_type, instruction, spanish_instruction in variant_specs:
            if variant_type == "speaking":
                text = f"{instruction} {base_text}"
            elif variant_type == "listening":
                text = f"{instruction} {base_text}"
            elif variant_type == "writing":
                text = f"{instruction} {base_text}"
            else:
                text = f"{instruction} {base_text}"
            all_cards.append({
                "deck": f"03_Languages::English::Variant_Pipeline::{variant_type.title()}",
                "scenario": f"{base_scenario} · {variant_type}",
                "text": text,
                "explanation": f"Reinforcement card for the same scenario using a {variant_type} exercise.",
                "usage": instruction,
                "spanish": f"{spanish_instruction} {base_spanish}",
                "tags": ["english", "variant_pipeline", variant_type],
                "source_text": base_text,
                "variant_type": variant_type,
            })

for variant_type, _, _ in variant_specs:
    subset = [c for c in all_cards if c["variant_type"] == variant_type]
    out_path = output_dir / variant_type / f"{variant_type}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(subset, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {len(subset)} {variant_type} cards to {out_path}")

print(f"Total generated cards: {len(all_cards)}")
