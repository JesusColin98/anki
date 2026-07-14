import json
from pathlib import Path

root = Path(r"C:\Users\jesus\anki")
index_path = root / "decks" / "index.json"

with open(index_path, "r", encoding="utf-8") as f:
    data = json.load(f)

existing_paths = {item["path"] for item in data.get("decks", [])}

scenarios = [
    "At the airport", "At the train station", "At the bus terminal", "At the hotel reception", "At the taxi stand",
    "At the rental car desk", "At the passport office", "At the embassy", "At the immigration desk", "At the tourist information desk",
    "At the metro station", "At the ferry terminal", "At the currency exchange", "At the pharmacy abroad", "At the hospital reception",
    "At the local police station", "At the post office", "At the bank", "At the utility office", "At the library",
    "At the gas station", "At the parking office", "At the bike rental", "At the travel agency", "At the customer service desk"
]
items = [
    "the gate", "the ticket", "the platform", "the reservation", "the luggage", "the passport", "the visa", "the room", "the taxi", "the receipt",
    "the transfer", "the schedule", "the refund", "the insurance", "the appointment", "the form", "the address", "the balance", "the invoice", "the service",
    "the map", "the parking spot", "the shuttle", "the itinerary", "the complaint"
]
patterns = [
    ("Could you tell me where {{c1::{item}}} is?", "¿Podrías decirme dónde está {item}?"),
    ("I need help with {{c1::{item}}}.", "Necesito ayuda con {item}."),
    ("Can you confirm {{c1::{item}}} for me?", "¿Puedes confirmar {item} por mí?"),
    ("Is {{c1::{item}}} included in the price?", "¿Está {item} incluido en el precio?"),
    ("How long does {{c1::{item}}} take?", "¿Cuánto tarda {item}?"),
    ("Where do I go for {{c1::{item}}}?", "¿Adónde voy para {item}?"),
    ("I’m trying to find {{c1::{item}}}.", "Estoy intentando encontrar {item}."),
    ("Do you know if {{c1::{item}}} is available?", "¿Sabes si {item} está disponible?"),
    ("Could you explain {{c1::{item}}} to me?", "¿Podrías explicarme {item}?"),
    ("I’m not sure about {{c1::{item}}}.", "No estoy seguro/a de {item}."),
]

cards = []
for idx, scenario in enumerate(scenarios):
    for jdx, (pattern, span_pattern) in enumerate(patterns):
        item = items[(idx + jdx) % len(items)]
        english = pattern.format(item=item)
        spanish = span_pattern.format(item=item)
        cards.append({
            "deck": "03_Languages::English::08_Real_Scenario_Expansion::09_Travel_and_Public_Services",
            "scenario": f"09_Travel_and_Public_Services: {scenario}",
            "text": english,
            "explanation": f"This is a practical phrase used in {scenario.lower()} to sound natural and useful in real conversations.",
            "usage": f"Useful for practicing realistic English in {scenario.lower()}.",
            "spanish": spanish,
            "tags": ["english", "real_scenario", "travel"]
        })

assert len(cards) == 250

path = root / "decks" / "03_Languages" / "English" / "08_Real_Scenario_Expansion" / "09_Travel_and_Public_Services" / "09_Travel_and_Public_Services.json"
path.parent.mkdir(parents=True, exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)
    f.write("\n")

rel_path = path.relative_to(root).as_posix()
if rel_path not in existing_paths:
    data["decks"].append({
        "deck": cards[0]["deck"],
        "path": rel_path,
        "cards_count": len(cards),
    })
    existing_paths.add(rel_path)

data["total_cards"] = sum(int(entry.get("cards_count", 0)) for entry in data.get("decks", []))
data["total_decks"] = len(data.get("decks", []))

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Created 250 travel and public services cards and updated the index.")
