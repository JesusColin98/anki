import json
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()

def fix_mismatches():
    # 1. 3-level to 4-level deck name/path updates
    updates = [
        {
            "src": "decks/02_AI_and_Data_Science/MLOps_and_LLMOps/Model_Deployment_and_Monitoring.json",
            "dst": "decks/02_AI_and_Data_Science/MLOps_and_LLMOps/Deployment/Model_Deployment_and_Monitoring.json",
            "deck": "02_AI_and_Data_Science::MLOps_and_LLMOps::Deployment::Model_Deployment_and_Monitoring"
        },
        {
            "src": "decks/02_AI_and_Data_Science/RAG_and_Advanced_Applied/RAG_and_AI_Product.json",
            "dst": "decks/02_AI_and_Data_Science/RAG_and_Advanced_Applied/RAG_Systems/RAG_and_AI_Product.json",
            "deck": "02_AI_and_Data_Science::RAG_and_Advanced_Applied::RAG_Systems::RAG_and_AI_Product"
        },
        {
            "src": "decks/02_AI_and_Data_Science/Responsible_AI/Responsible_AI_Core.json",
            "dst": "decks/02_AI_and_Data_Science/Responsible_AI/Governance/Responsible_AI_Core.json",
            "deck": "02_AI_and_Data_Science::Responsible_AI::Governance::Responsible_AI_Core"
        },
        {
            "src": "decks/05_Soft_Skills_and_Leadership/Leadership_Core/Leadership_Core_Concepts.json",
            "dst": "decks/05_Soft_Skills_and_Leadership/Leadership_Core/Core_Concepts/Leadership_Core_Concepts.json",
            "deck": "05_Soft_Skills_and_Leadership::Leadership_Core::Core_Concepts::Leadership_Core_Concepts"
        },
        {
            "src": "decks/03_Languages/English/Phonetics/Connected_Speech_Advanced/Connected_Speech_Advanced.json",
            "dst": "decks/03_Languages/English/Phonetics/Connected_Speech_Advanced.json",
            "deck": "03_Languages::English::Phonetics::Connected_Speech_Advanced"
        }
    ]
    
    for item in updates:
        src_path = BASE_DIR / item["src"]
        dst_path = BASE_DIR / item["dst"]
        
        if src_path.exists():
            print(f"Moving & updating: {src_path.name} -> {item['dst']}")
            with open(src_path, "r", encoding="utf-8") as f:
                cards = json.load(f)
                
            for card in cards:
                card["deck"] = item["deck"]
                
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dst_path, "w", encoding="utf-8") as f:
                json.dump(cards, f, indent=2, ensure_ascii=False)
                
            src_path.unlink()
            # Clean up empty parent directories of src
            parent = src_path.parent
            while parent != BASE_DIR / "decks":
                if not any(parent.iterdir()):
                    print(f"Removing empty folder: {parent.relative_to(BASE_DIR)}")
                    parent.rmdir()
                    parent = parent.parent
                else:
                    break
        else:
            print(f"Skipping {item['src']} (already moved or missing)")
            
    # 2. Merging 5-level decks into 4-level target decks
    merges = [
        {
            "src": "decks/03_Languages/English/06_Leadership_and_Executive_English/Coaching_and_Performance/Coaching_and_Performance.json",
            "dst": "decks/03_Languages/English/Leadership_and_Executive_English/Delegation_and_Accountability.json",
            "deck": "03_Languages::English::Leadership_and_Executive_English::Delegation_and_Accountability"
        },
        {
            "src": "decks/03_Languages/English/06_Leadership_and_Executive_English/Executive_Updates/Executive_Updates.json",
            "dst": "decks/03_Languages/English/Leadership_and_Executive_English/Executive_Updates.json",
            "deck": "03_Languages::English::Leadership_and_Executive_English::Executive_Updates"
        },
        {
            "src": "decks/03_Languages/English/07_English_for_Support_and_Ops/Incident_Communication/Incident_Communication.json",
            "dst": "decks/03_Languages/English/Support_and_Operations_English/Incident_Communication.json",
            "deck": "03_Languages::English::Support_and_Operations_English::Incident_Communication"
        }
    ]
    
    for item in merges:
        src_path = BASE_DIR / item["src"]
        dst_path = BASE_DIR / item["dst"]
        
        if src_path.exists():
            print(f"Merging: {src_path.relative_to(BASE_DIR)} -> {dst_path.relative_to(BASE_DIR)}")
            with open(src_path, "r", encoding="utf-8") as f:
                src_cards = json.load(f)
                
            if dst_path.exists():
                with open(dst_path, "r", encoding="utf-8") as f:
                    dst_cards = json.load(f)
            else:
                dst_cards = []
                
            # Update deck name and merge
            for card in src_cards:
                card["deck"] = item["deck"]
                # Prevent duplicates during merge
                if card["text"] not in [c["text"] for c in dst_cards]:
                    dst_cards.append(card)
                    
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dst_path, "w", encoding="utf-8") as f:
                json.dump(dst_cards, f, indent=2, ensure_ascii=False)
                
            src_path.unlink()
            # Clean up empty parent directories of src
            parent = src_path.parent
            while parent != BASE_DIR / "decks":
                if not any(parent.iterdir()):
                    print(f"Removing empty folder: {parent.relative_to(BASE_DIR)}")
                    parent.rmdir()
                    parent = parent.parent
                else:
                    break
        else:
            print(f"Skipping merge of {item['src']} (already merged or missing)")

if __name__ == "__main__":
    fix_mismatches()
