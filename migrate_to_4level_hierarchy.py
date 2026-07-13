#!/usr/bin/env python3
"""Migrate Anki Decks to a 4-Level Deep Hierarchy across 6 Main Scalable Pillars.

6 Main Pillars:
1. 01_Cloud_and_Infrastructure (Networking, Cybersecurity, Cloud, Systems Engineering)
2. 02_AI_and_Data_Science (Classical ML, LLMs, Agentic Systems, RAG, MLOps)
3. 03_Languages (English, Spanish, Chinese, French, German, Japanese, Korean, Italian, Portuguese, Russian, News)
4. 04_Social_and_Humanities (Philosophy, History, Sociology, Conversational Psychology)
5. 05_Soft_Skills_and_Leadership (Persuasion, Listening, Presence, Customer Support, Etiquette, Storytelling)
6. 06_Business_and_Productivity (Business Strategy, Productivity, Learning Methods)

Reorganizes all subdecks into 4-level deep directory paths and updates
deck names and card metadata accordingly.
"""

import json
from pathlib import Path
import shutil
import sys

BASE_DIR = Path(__file__).parent.resolve()
DECKS_DIR = BASE_DIR / "decks"
MONOLITH_JSON = BASE_DIR / "anki_cards_database.json"

VALID_PILLARS = {
    "01_Cloud_and_Infrastructure",
    "02_AI_and_Data_Science",
    "03_Languages",
    "04_Social_and_Humanities",
    "05_Soft_Skills_and_Leadership",
    "06_Business_and_Productivity",
}


def map_deck_to_6pillars(old_deck: str) -> str:
    parts = old_deck.split("::")
    root = parts[0]

    # Handle 5-pillar deck names
    if root == "01_Infrastructure_and_Cloud":
        cat, sub, name = parts[1], parts[2], parts[3]
        if cat == "Networking_Security":
            if "Fundamentals" in sub or "Fundamentals" in name:
                return f"01_Cloud_and_Infrastructure::Networking::Fundamentals::{name}"
            elif "Reconnaissance" in sub or "Reconnaissance" in name:
                return f"01_Cloud_and_Infrastructure::Cybersecurity::Reconnaissance::{name}"
            elif "Defense" in sub or "Defense" in name:
                return f"01_Cloud_and_Infrastructure::Cybersecurity::Defense_Evasion::{name}"
        elif cat == "Tech_Map_2026":
            return f"01_Cloud_and_Infrastructure::Systems_Engineering::Infrastructure::{name}"
    elif root == "02_AI_and_Hardware":
        cat, sub, name = parts[1], parts[2], parts[3]
        if cat == "AI_Learning_Path":
            return f"02_AI_and_Data_Science::AI_Learning_Path::{sub}::{name}"
        elif cat == "Tech_Map_2026":
            return f"02_AI_and_Data_Science::Tech_Map_2026::{sub}::{name}"
        elif cat == "Books_Path":
            return f"02_AI_and_Data_Science::Books::{sub}::{name}"
    elif root == "03_Languages_and_Communication":
        lang, cat, name = parts[1], parts[2], parts[3]
        return f"03_Languages::{lang}::{cat}::{name}"
    elif root == "04_Psychology_and_Soft_Skills":
        cat, sub, name = parts[1], parts[2], parts[3]
        if cat == "Social_Skills" and ("Conversational" in sub or "07_Conversational" in name):
            return f"04_Social_and_Humanities::Psychology::Conversational::{name}"
        elif cat == "Books_Path" and "Communication" in sub:
            return f"05_Soft_Skills_and_Leadership::Books::Communication::{name}"
        return f"05_Soft_Skills_and_Leadership::{cat}::{sub}::{name}"
    elif root == "05_Knowledge_and_Philosophy":
        cat, sub, name = parts[1], parts[2], parts[3]
        if cat == "Philosophy":
            return f"04_Social_and_Humanities::Philosophy::{sub}::{name}"
        elif cat == "Books_Path" and "Philosophy" in sub:
            return f"04_Social_and_Humanities::Books::Philosophy::{name}"
        return f"06_Business_and_Productivity::{cat}::{sub}::{name}"

    # Handle legacy root names
    if root == "Networking_Security":
        sub = parts[1]
        if "Fundamentals" in sub:
            return f"01_Cloud_and_Infrastructure::Networking::Fundamentals::{sub}"
        elif "Reconnaissance" in sub:
            return f"01_Cloud_and_Infrastructure::Cybersecurity::Reconnaissance::{sub}"
        elif "Defense" in sub:
            return f"01_Cloud_and_Infrastructure::Cybersecurity::Defense_Evasion::{sub}"
        return f"01_Cloud_and_Infrastructure::Networking::General::{sub}"
    elif root == "Tech_Map_2026" and parts[1] == "05_Infrastructure_Science":
        return f"01_Cloud_and_Infrastructure::Systems_Engineering::Infrastructure::{parts[1]}"
    elif root == "AI_Learning_Path":
        if len(parts) == 2:
            sub = parts[1]
            if sub.startswith("01_Classical_ML"):
                return f"02_AI_and_Data_Science::Classical_ML::Overview::{sub}"
            elif sub.startswith("02_LLM"):
                return f"02_AI_and_Data_Science::LLM_Systems::Fundamentals::{sub}"
            elif sub.startswith("03_Advanced_LLM"):
                return f"02_AI_and_Data_Science::LLM_Systems::Advanced::{sub}"
            elif sub.startswith("04_Agentic"):
                return f"02_AI_and_Data_Science::Agentic_Systems::Overview::{sub}"
        elif len(parts) == 3:
            cat, sub = parts[1], parts[2]
            if cat.startswith("01_Classical"):
                return f"02_AI_and_Data_Science::Classical_ML::{cat[3:]}::{sub}"
            elif cat.startswith("04_Agentic"):
                return f"02_AI_and_Data_Science::Agentic_Systems::{cat[3:]}::{sub}"
    elif root == "Tech_Map_2026":
        sub = parts[1]
        if sub == "01_AI_Agents_Autonomy":
            return f"02_AI_and_Data_Science::Agentic_Systems::Autonomy::{sub}"
        elif sub == "02_Reasoning_LLMs":
            return f"02_AI_and_Data_Science::LLM_Systems::Reasoning::{sub}"
        elif sub == "03_Advanced_RAG":
            return f"02_AI_and_Data_Science::RAG_Systems::Advanced::{sub}"
        elif sub == "04_Agentic_Dev_IDEs":
            return f"02_AI_and_Data_Science::Agentic_Systems::IDEs::{sub}"
        elif sub == "06_MLOps_Guardrails":
            return f"02_AI_and_Data_Science::MLOps::Guardrails::{sub}"
    elif root == "Books_Path" and parts[1] in ("04_AI_Engineering", "06_AI_ML_Essential_Library"):
        sub = parts[1]
        topic = "Engineering" if "Engineering" in sub else "Library"
        return f"02_AI_and_Data_Science::Books::{topic}::{sub}"
    elif root in [
        "Chinese",
        "English",
        "French",
        "German",
        "Italian",
        "Japanese",
        "Korean",
        "Portuguese",
        "Russian",
        "Spanish",
    ]:
        if len(parts) == 2:
            return f"03_Languages::{root}::{parts[1]}::General"
        elif len(parts) == 3:
            return f"03_Languages::{root}::{parts[1]}::{parts[2]}"
    elif root == "News_Scraped":
        sub = parts[1] if len(parts) > 1 else "General"
        return f"03_Languages::News_Scraped::Articles::{sub}"
    elif root == "Philosophy":
        if len(parts) == 3:
            return f"04_Social_and_Humanities::Philosophy::{parts[1]}::{parts[2]}"
    elif root == "Social_Skills" and len(parts) == 2 and parts[1] == "07_Conversational_Psychology":
        return f"04_Social_and_Humanities::Psychology::Conversational::{parts[1]}"
    elif root == "Books_Path" and parts[1] == "05_Philosophy_Meaning":
        return f"04_Social_and_Humanities::Books::Philosophy::{parts[1]}"
    elif root == "Social_Skills":
        if len(parts) == 2:
            sub = parts[1]
            topic = sub.split("_", 1)[-1] if "_" in sub else sub
            return f"05_Soft_Skills_and_Leadership::Social_Skills::{topic}::{sub}"
        elif len(parts) == 3:
            return f"05_Soft_Skills_and_Leadership::Social_Skills::{parts[1]}::{parts[2]}"
    elif root == "SoftSkills":
        sub = parts[1] if len(parts) > 1 else "General"
        return f"05_Soft_Skills_and_Leadership::SoftSkills::{sub}::General"
    elif root == "Books_Path" and parts[1] == "02_Communication_Influence":
        return f"05_Soft_Skills_and_Leadership::Books::Communication::{parts[1]}"
    elif root == "Books_Path":
        sub = parts[1]
        if sub == "01_Business_Strategy":
            return f"06_Business_and_Productivity::Business::Strategy::{sub}"
        elif sub == "03_Learning_Productivity":
            return f"06_Business_and_Productivity::Productivity::Learning::{sub}"

    if parts[0] in VALID_PILLARS and len(parts) == 4:
        return old_deck

    raise ValueError(f"Unable to map old deck: {old_deck}")


def main():
    index_file = DECKS_DIR / "index.json"
    if not index_file.exists():
        print(f"Error: {index_file} not found.", file=sys.stderr)
        sys.exit(1)

    with open(index_file, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    all_cards_map = {}
    for entry in index_data["decks"]:
        old_deck = entry["deck"]
        rel_path = entry["path"]
        file_path = BASE_DIR / rel_path

        if not file_path.exists():
            print(f"Warning: File {file_path} missing.", file=sys.stderr)
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            cards = json.load(f)

        new_deck = map_deck_to_6pillars(old_deck)
        depth = len(new_deck.split("::"))
        if depth != 4:
            raise ValueError(f"Mapped deck '{new_deck}' does not have 4 levels (has {depth}).")

        for card in cards:
            card["deck"] = new_deck

        all_cards_map.setdefault(new_deck, []).extend(cards)

    # Clean existing top-level directories in decks/
    for p in DECKS_DIR.iterdir():
        if p.is_dir():
            shutil.rmtree(p)

    index_entries = []
    total_cards_count = 0
    all_migrated_cards = []

    for new_deck_name, deck_cards in sorted(all_cards_map.items()):
        rel_file_path = new_deck_name.replace("::", "/") + ".json"
        target_file = DECKS_DIR / rel_file_path
        target_file.parent.mkdir(parents=True, exist_ok=True)

        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(deck_cards, f, indent=2, ensure_ascii=False)

        total_cards_count += len(deck_cards)
        all_migrated_cards.extend(deck_cards)

        index_entries.append({
            "deck": new_deck_name,
            "path": f"decks/{rel_file_path}",
            "cards_count": len(deck_cards),
        })

    # Write new global index
    new_index_data = {
        "total_cards": total_cards_count,
        "total_decks": len(index_entries),
        "decks": index_entries,
    }
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(new_index_data, f, indent=2, ensure_ascii=False)

    # Update monolith JSON as well
    with open(MONOLITH_JSON, "w", encoding="utf-8") as f:
        json.dump(all_migrated_cards, f, indent=2, ensure_ascii=False)

    print("=== MIGRATION COMPLETE (6 PILLARS) ===")
    print(f"Total decks migrated: {len(index_entries)}")
    print(f"Total cards migrated: {total_cards_count}")
    print(f"New index saved to: {index_file}")


if __name__ == "__main__":
    main()
