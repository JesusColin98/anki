import json
from pathlib import Path
from urllib.parse import quote

root = Path(r"C:\Users\jesus\anki")
index_path = root / "decks" / "index.json"

with open(index_path, "r", encoding="utf-8") as f:
    data = json.load(f)

existing_paths = {item["path"] for item in data.get("decks", [])}

prompts = [
    "Give a short update on your current project in a natural way.",
    "Explain a recent challenge you handled at work and how you solved it.",
    "Describe your typical daily routine in a clear and engaging way.",
    "Tell a story about a mistake you learned from and how you improved.",
    "Explain how you would handle a difficult customer call.",
    "Describe a place you would love to visit and why.",
    "Share a simple opinion about the best way to learn a new skill.",
    "Talk about a habit that helps you stay productive.",
    "Explain what you would do if you had more free time this weekend.",
    "Describe a small decision that changed your life for the better.",
]

cards = []
for idx, prompt in enumerate(prompts * 8):
    scenario = f"Speaking Practice {idx + 1}"
    deck = "03_Languages::English::Speaking::01_Speaking_Practice"
    audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    practice_url = f"file:///{root.as_posix().replace('\\', '/')}/scratch/speaking_practice_app.html?prompt={quote(prompt)}"
    cards.append({
        "deck": deck,
        "text": prompt,
        "prompt": prompt,
        "scenario": scenario,
        "explanation": "Use this card to practice spoken fluency, rhythm, and confidence. Listen to the reference audio, then record yourself and compare your delivery.",
        "usage": "Speak for 20 to 30 seconds, focus on stress and pacing, and record a clean take.",
        "spanish": f"Practica esta idea en inglés y grábate para mejorar tu pronunciación y fluidez.",
        "audio": f'<audio controls preload="none"><source src="{audio_url}" type="audio/mpeg"></audio>',
        "practice_link": f'<a href="{practice_url}" target="_blank">🎙️ Open recorder</a>',
        "practice_url": practice_url,
        "model_audio_url": audio_url,
        "recording_hint": "Record a first take, then listen back and improve stress, pacing, and clarity.",
        "model_name": "Engaging_Speaking_Model",
        "tags": ["english", "speaking", "pronunciation", "self_recording"],
    })

path = root / "decks" / "03_Languages" / "English" / "Speaking" / "01_Speaking_Practice" / "01_Speaking_Practice.json"
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

print(f"Created {len(cards)} speaking practice cards and updated the index.")
