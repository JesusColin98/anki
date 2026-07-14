import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

root = Path(r"C:\Users\jesus\anki")
source_dir = root / "decks" / "03_Languages" / "English" / "08_Real_Scenario_Expansion"
output_dir = root / "decks" / "03_Languages" / "English" / "Variant_Pipeline"
output_dir.mkdir(parents=True, exist_ok=True)
index_path = root / "decks" / "index.json"

variant_specs = [
    {
        "variant_type": "speaking",
        "instruction": "Say this out loud and record yourself.",
        "spanish_instruction": "Practica esta idea en voz alta.",
        "deck_suffix": "Speaking",
    },
    {
        "variant_type": "listening",
        "instruction": "Listen and complete the phrase in context.",
        "spanish_instruction": "Escucha y completa la idea.",
        "deck_suffix": "Listening",
    },
    {
        "variant_type": "writing",
        "instruction": "Write a short response using the same idea.",
        "spanish_instruction": "Escribe una respuesta corta usando la misma idea.",
        "deck_suffix": "Writing",
    },
    {
        "variant_type": "dialogue",
        "instruction": "Complete the dialogue naturally.",
        "spanish_instruction": "Completa el diálogo de forma natural.",
        "deck_suffix": "Dialogue",
    },
    {
        "variant_type": "roleplay",
        "instruction": "Play the next turn of the conversation naturally.",
        "spanish_instruction": "Haz el siguiente turno de la conversación de forma natural.",
        "deck_suffix": "Roleplay",
    },
    {
        "variant_type": "error_correction",
        "instruction": "Find and fix the unnatural or incorrect phrasing.",
        "spanish_instruction": "Encuentra y corrige la frase poco natural o incorrecta.",
        "deck_suffix": "ErrorCorrection",
    },
    {
        "variant_type": "paraphrase",
        "instruction": "Rephrase the idea more naturally or more formally.",
        "spanish_instruction": "Reformula la idea de forma más natural o más formal.",
        "deck_suffix": "Paraphrase",
    },
    {
        "variant_type": "summary",
        "instruction": "Summarize the idea in one short sentence.",
        "spanish_instruction": "Resume la idea en una frase corta.",
        "deck_suffix": "Summary",
    },
]


def normalize_text(value: str) -> str:
    return " ".join(str(value or "").split())


def compute_source_hash(card: dict, source_path: Path) -> str:
    payload = f"{source_path.as_posix()}|{normalize_text(card.get('text', ''))}|{normalize_text(card.get('scenario', ''))}|{normalize_text(card.get('spanish', ''))}"
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]


def infer_skill_area(source_path: Path) -> str:
    path_name = source_path.as_posix().lower()
    if "interview" in path_name:
        return "interviews"
    if "phone" in path_name or "customer" in path_name:
        return "customer_service"
    if "health" in path_name or "emergency" in path_name:
        return "health"
    if "education" in path_name or "academic" in path_name:
        return "education"
    return "general_scenario"


def infer_difficulty(source_path: Path) -> str:
    return "intermediate"


def load_index() -> dict:
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index(index_data: dict) -> None:
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def update_index(index_data: dict, deck_name: str, deck_path: Path, card_count: int) -> None:
    existing_paths = {entry.get("path") for entry in index_data.get("decks", [])}
    rel_path = deck_path.relative_to(root).as_posix()
    if rel_path not in existing_paths:
        index_data.setdefault("decks", []).append({
            "deck": deck_name,
            "path": rel_path,
            "cards_count": card_count,
        })
    index_data["total_cards"] = sum(int(entry.get("cards_count", 0)) for entry in index_data.get("decks", []))
    index_data["total_decks"] = len(index_data.get("decks", []))


source_files = sorted([p for p in source_dir.rglob("*.json") if p.name != "index.json"])
index_data = load_index()
manifest_entries = []
all_cards = []

for source_file in source_files:
    with open(source_file, "r", encoding="utf-8") as f:
        cards = json.load(f)

    for card in cards[:20]:
        base_text = normalize_text(card.get("text", ""))
        base_scenario = normalize_text(card.get("scenario", "Scenario"))
        base_spanish = normalize_text(card.get("spanish", ""))
        source_hash = compute_source_hash(card, source_file)
        source_id = f"src:{source_hash}"
        scenario_id = base_scenario.lower().replace(" ", "_").replace("/", "_")
        skill_area = infer_skill_area(source_file)
        difficulty = infer_difficulty(source_file)

        for variant in variant_specs:
            variant_type = variant["variant_type"]
            instruction = variant["instruction"]
            spanish_instruction = variant["spanish_instruction"]
            text = f"{instruction} {base_text}"
            explanation = f"Reinforcement card for the same scenario using a {variant_type} exercise."
            usage = instruction
            spanish = f"{spanish_instruction} {base_spanish}"
            if variant_type == "roleplay":
                text = f"Roleplay: {base_text}"
                explanation = f"Practice a two-turn exchange around the same scenario and keep the response natural."
            elif variant_type == "error_correction":
                text = f"Correct this phrasing: {base_text}"
                explanation = f"Focus on naturalness, correctness, and useful phrasing for the same scenario."
            elif variant_type == "paraphrase":
                text = f"Paraphrase this: {base_text}"
                explanation = f"Reformulate the same meaning with a different level of formality or naturalness."
            elif variant_type == "summary":
                text = f"Summarize this idea: {base_text}"
                explanation = f"Condense the same idea into a short, clear sentence."
            deck_name = f"03_Languages::English::Variant_Pipeline::{variant['deck_suffix']}"

            card_entry = {
                "deck": deck_name,
                "scenario": f"{base_scenario} · {variant_type}",
                "text": text,
                "explanation": explanation,
                "usage": usage,
                "spanish": spanish,
                "tags": ["english", "variant_pipeline", variant_type, skill_area],
                "source_text": base_text,
                "source_spanish": base_spanish,
                "source_id": source_id,
                "source_file": source_file.relative_to(root).as_posix(),
                "scenario_id": scenario_id,
                "skill_area": skill_area,
                "difficulty": difficulty,
                "variant_type": variant_type,
                "source_hash": source_hash,
                "metadata_version": 1,
            }
            all_cards.append(card_entry)
            manifest_entries.append({
                "source_id": source_id,
                "source_file": source_file.relative_to(root).as_posix(),
                "variant_type": variant_type,
                "deck": deck_name,
                "scenario_id": scenario_id,
                "skill_area": skill_area,
                "difficulty": difficulty,
            })

for variant in variant_specs:
    variant_type = variant["variant_type"]
    deck_name = f"03_Languages::English::Variant_Pipeline::{variant['deck_suffix']}"
    subset = [card for card in all_cards if card["variant_type"] == variant_type]
    out_path = output_dir / variant_type / f"{variant_type}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(subset, f, indent=2, ensure_ascii=False)
        f.write("\n")
    update_index(index_data, deck_name, out_path, len(subset))
    print(f"Wrote {len(subset)} {variant_type} cards to {out_path}")

manifest_path = output_dir / "manifest.json"
manifest_payload = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "source_root": source_dir.relative_to(root).as_posix(),
    "variant_specs": [v["variant_type"] for v in variant_specs],
    "relationships": manifest_entries,
}
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest_payload, f, indent=2, ensure_ascii=False)
    f.write("\n")

save_index(index_data)
print(f"Total generated cards: {len(all_cards)}")
print(f"Manifest written to {manifest_path}")
