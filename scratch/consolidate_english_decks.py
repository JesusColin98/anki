import os
import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
ENGLISH_DIR = BASE_DIR / "decks" / "03_Languages" / "English"
LP_DIR = ENGLISH_DIR / "Learning_Paths"

# Define Learning Path subdecks (4 levels deep)
LP_DECKS = {
    "daily": "03_Languages::English::Learning_Paths::01_Daily_and_Social",
    "workplace": "03_Languages::English::Learning_Paths::02_Workplace_and_Service",
    "interview": "03_Languages::English::Learning_Paths::03_Interview_and_Career",
    "academic": "03_Languages::English::Learning_Paths::04_Academic_and_Health",
}

def get_target_lp(file_path, card=None):
    fp = file_path.replace("\\", "/").lower()
    
    # Check filename first
    if "interview" in fp or "leadership" in fp or "executive" in fp or "director" in fp or "manager" in fp:
        return LP_DECKS["interview"]
    elif "workplace" in fp or "phone_calls" in fp or "professional" in fp or "support" in fp or "incident" in fp:
        return LP_DECKS["workplace"]
    elif "health" in fp or "emergency" in fp or "academic" in fp or "philosophical" in fp or "education" in fp:
        return LP_DECKS["academic"]
    elif "daily" in fp or "social" in fp or "travel" in fp or "cafe" in fp or "hotel" in fp or "airport" in fp or "grocery" in fp or "jokes" in fp or "beginner" in fp or "greeting" in fp:
        return LP_DECKS["daily"]
        
    # Check card content if file path is ambiguous
    if card:
        source_file = card.get("source_file", "").replace("\\", "/").lower()
        if "05_interviews" in source_file:
            return LP_DECKS["interview"]
        elif "02_workplace" in source_file or "06_phone_calls" in source_file:
            return LP_DECKS["workplace"]
        elif "07_health" in source_file or "08_education" in source_file:
            return LP_DECKS["academic"]
            
    # Default fallback
    return LP_DECKS["daily"]

def main():
    print("=== STARTING ENGLISH DECK CONSOLIDATION ===")
    
    # 1. Ensure target LP directories exist
    for lp in ["01_Daily_and_Social", "02_Workplace_and_Service", "03_Interview_and_Career", "04_Academic_and_Health"]:
        (LP_DIR / lp).mkdir(parents=True, exist_ok=True)
        
    # 2. Find all directories to scan
    folders_to_scan = [
        "01_Daily_Life",
        "02_Professional",
        "03_Socializing",
        "04_Storytelling_and_Expression",
        "05_Academic_and_Philosophical",
        "A1_Beginner",
        "Daily_and_Social",
        "Leadership_and_Executive_English",
        "Support_and_Operations_English",
        "Speaking",
        "Case_Variants",
        "Variant_Pipeline",
    ]
    
    moved_count = 0
    
    for folder_name in folders_to_scan:
        folder_path = ENGLISH_DIR / folder_name
        if not folder_path.exists():
            continue
            
        print(f"Scanning folder: {folder_name}...")
        for root, dirs, files in os.walk(folder_path):
            # Sort dirs and files to be deterministic
            dirs.sort()
            for file in sorted(files):
                if file.endswith(".json") and file not in ["index.json", "manifest.json"]:
                    src_file = Path(root) / file
                    
                    # Read cards
                    with open(src_file, "r", encoding="utf-8") as f:
                        try:
                            cards = json.load(f)
                        except Exception as e:
                            print(f"  [-] Error loading {file}: {e}")
                            continue
                            
                    if not cards:
                        continue
                        
                    # Determine target LP and subfolder
                    target_deck = get_target_lp(str(src_file), cards[0])
                    
                    # Map deck to subfolder path
                    if target_deck == LP_DECKS["daily"]:
                        dest_sub = LP_DIR / "01_Daily_and_Social"
                    elif target_deck == LP_DECKS["workplace"]:
                        dest_sub = LP_DIR / "02_Workplace_and_Service"
                    elif target_deck == LP_DECKS["interview"]:
                        dest_sub = LP_DIR / "03_Interview_and_Career"
                    else:
                        dest_sub = LP_DIR / "04_Academic_and_Health"
                        
                    # If it's from Variant_Pipeline or Case_Variants, keep it under a variants folder or suffix to prevent name collisions
                    dest_filename = file
                    if "Variant_Pipeline" in str(src_file) or "Case_Variants" in str(src_file):
                        # Find the parent folder name
                        parent_name = src_file.parent.name
                        dest_filename = f"variant_{parent_name}_{file}"
                        
                    dest_file = dest_sub / dest_filename
                    
                    # Update all cards in this file
                    for card in cards:
                        card["deck"] = target_deck
                        
                    # Write updated cards to new location
                    with open(dest_file, "w", encoding="utf-8") as f:
                        json.dump(cards, f, indent=2, ensure_ascii=False)
                        f.write("\n")
                        
                    print(f"  [->] Consolidated: {src_file.relative_to(BASE_DIR)} -> {dest_file.relative_to(BASE_DIR)}")
                    moved_count += 1
                    
    # 3. Clean up the scanned directories (delete them)
    print("\nCleaning up legacy directories...")
    for folder_name in folders_to_scan:
        folder_path = ENGLISH_DIR / folder_name
        if not folder_path.exists():
            continue
            
        if folder_name == "Variant_Pipeline":
            # Just remove subdirectories under Variant_Pipeline
            for item in folder_path.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                    print(f"  [-] Removed folder: {item.relative_to(BASE_DIR)}")
        else:
            shutil.rmtree(folder_path)
            print(f"  [-] Removed folder: {folder_path.relative_to(BASE_DIR)}")
            
    print(f"\nConsolidation complete! Successfully consolidated {moved_count} JSON files.")
