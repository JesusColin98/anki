#!/usr/bin/env python3
import json
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
DECKS_DIR = BASE_DIR / "decks"

# Define the clean 4-level mappings
MAPPINGS = {
    # Old Rel Path -> (New Rel Path, New 4-Level Deck Key)
    "04_Social_and_Humanities/Books/05_philosophy_meaning.json": (
        "04_Social_and_Humanities/Philosophy/Book_Summaries/philosophy_of_meaning.json",
        "04_Social_and_Humanities::Philosophy::Book_Summaries::Philosophy_Of_Meaning"
    ),
    "02_AI_and_Data_Science/Tech_Map_2026/06_mlops_guardrails.json": (
        "02_AI_and_Data_Science/MLOps_and_LLMOps/Governance/mlops_guardrails.json",
        "02_AI_and_Data_Science::MLOps_and_LLMOps::Governance::Mlops_Guardrails"
    ),
    "02_AI_and_Data_Science/08_Advanced_AI_Engineering/14_security_privacy_and_adversarial_ai.json": (
        "02_AI_and_Data_Science/AI_Engineering/Security_And_Privacy/security_privacy_and_adversarial_ai.json",
        "02_AI_and_Data_Science::AI_Engineering::Security_And_Privacy::Security_Privacy_And_Adversarial_Ai"
    ),
    "02_AI_and_Data_Science/08_Advanced_AI_Engineering/15_experimentation_data_pipelines_and_feature_stores.json": (
        "02_AI_and_Data_Science/AI_Engineering/Data_Pipelines/experimentation_data_pipelines_and_feature_stores.json",
        "02_AI_and_Data_Science::AI_Engineering::Data_Pipelines::Experimentation_Data_Pipelines_And_Feature_Stores"
    ),
    "02_AI_and_Data_Science/08_Advanced_AI_Engineering/18_ml_system_design_and_platforms.json": (
        "02_AI_and_Data_Science/AI_Engineering/System_Design/ml_system_design_and_platforms.json",
        "02_AI_and_Data_Science::AI_Engineering::System_Design::Ml_System_Design_And_Platforms"
    )
}

def main():
    print("=== CLEANING DECK DEPTH HIERARCHY ===")
    for old_rel, (new_rel, new_deck) in MAPPINGS.items():
        old_path = DECKS_DIR / old_rel
        new_path = DECKS_DIR / new_rel
        
        if not old_path.exists():
            print(f"Skipping {old_rel} (does not exist or already moved)")
            continue
            
        print(f"Moving {old_rel} -> {new_rel}...")
        
        # Load content
        with open(old_path, "r", encoding="utf-8") as f:
            cards = json.load(f)
            
        # Update deck key in all cards
        for card in cards:
            card["deck"] = new_deck
            if "metadata" in card:
                card["metadata"]["pillar"] = new_deck.split("::")[0]
                
        # Create parent directories
        new_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save content
        with open(new_path, "w", encoding="utf-8") as f:
            json.dump(cards, f, indent=2, ensure_ascii=False)
            
        # Delete old file
        os.remove(old_path)
        
        # Clean empty old directories if any
        parent = old_path.parent
        while parent != DECKS_DIR:
            if parent.exists() and len(os.listdir(parent)) == 0:
                print(f"Removing empty parent directory: {parent.relative_to(DECKS_DIR)}")
                os.rmdir(parent)
            parent = parent.parent

    print("[SUCCESS] All non-conforming decks migrated to clean 4-level structures.")

if __name__ == "__main__":
    main()
