import json
import re
import os

def audit_database():
    db_path = "anki_cards_database.json"
    if not os.path.exists(db_path):
        print("Database not found.")
        return
        
    with open(db_path, "r", encoding="utf-8") as f:
        cards = json.load(f)
        
    print(f"Loaded {len(cards)} cards for audit.")
    
    cloze_violations = 0
    answer_length_violations = 0
    short_prompt_violations = 0
    long_explanation_violations = 0
    
    for i, card in enumerate(cards):
        # We need to reconstruct flat structure to check easily
        flat_data = {
            "deck": card.get("deck"),
            "id": card.get("id"),
            "template": card.get("template"),
            **card.get("metadata", {}),
            **card.get("content", {}),
            **card.get("mnemonics", {}),
            **card.get("interactivity", {})
        }
        
        text = flat_data.get("text", "")
        explanation = flat_data.get("explanation", "")
        spanish = flat_data.get("spanish", "")
        
        # Rule 1: Too many clozes (> 2)
        clozes = re.findall(r"\{\{c\d+::.*?\}\}", text)
        distinct_clozes = set(re.findall(r"\{\{c(\d+)::", text))
        if len(clozes) > 2:
            cloze_violations += 1
            
        # Rule 2: Cloze replacement text too long (> 150 chars)
        for cloze in clozes:
            content_match = re.search(r"\{\{c\d+::(.*?)\}\}", cloze)
            if content_match:
                cloze_content = content_match.group(1)
                if len(cloze_content) > 150:
                    answer_length_violations += 1
                    break
                    
        # Rule 3: Text prompt too short (< 15 chars)
        # Strip clozes and HTML tags
        clean_text = re.sub(r"\{\{c\d+::(.*?)\}\}", r"\1", text)
        clean_text = re.sub(r"<[^>]+>", "", clean_text).strip()
        if len(clean_text) < 15:
            short_prompt_violations += 1
            
        # Rule 4: Long explanation without tabs (> 600 chars)
        if len(explanation) > 600 and "tabs-container" not in explanation and "tab-btn" not in explanation:
            long_explanation_violations += 1
            
    print("\n=== COGNITIVE AUDIT RESULTS ===")
    print(f"Total Cloze Violations (> 2 clozes): {cloze_violations}")
    print(f"Total Cloze Answer Length Violations (> 150 chars): {answer_length_violations}")
    print(f"Total Short Prompt Violations (< 15 chars): {short_prompt_violations}")
    print(f"Total Long Explanation Violations (> 600 chars without tabs): {long_explanation_violations}")

if __name__ == "__main__":
    audit_database()
