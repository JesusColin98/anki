import json
import re
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from card_validator import sanitize_and_validate_card

def extract_core_term(scenario):
    # Remove emojis and split by delimiters
    clean = re.sub(r'[^\w\s\-\:]', '', scenario)
    parts = re.split(r'[\:\-]', clean)
    # Return the last part or the most significant term
    term = parts[-1].strip()
    return term

def find_overlap_words(text, spanish):
    # Find substrings of at least 3 characters that are in both text and spanish
    # but ignoring common Spanish small words like 'del', 'los', 'con', 'para'
    ignore = {'con', 'del', 'los', 'las', 'por', 'para', 'una', 'este', 'esta', 'como', 'pero', 'mas', 'muy'}
    
    # We look for word sequences from text that are present in spanish
    text_words = re.findall(r'[a-zA-Z\’\u2019]+', text)
    matches = []
    
    # Try finding multi-word matches first
    for length in [3, 2, 1]:
        for i in range(len(text_words) - length + 1):
            phrase = " ".join(text_words[i:i+length])
            if len(phrase) < 3:
                continue
            if phrase.lower() in ignore:
                continue
            # Escape regex chars and search in Spanish
            escaped = re.escape(phrase)
            if re.search(r'\b' + escaped + r'\b', spanish, re.IGNORECASE):
                matches.append(phrase)
                
    if matches:
        # Return the longest matching phrase
        return max(matches, key=len)
    return None

def repair_card(card):
    text = card.get("text", "")
    spanish = card.get("spanish", "")
    scenario = card.get("scenario", "")
    
    # Try 1: Find English overlap word in Spanish (for Language decks)
    overlap = find_overlap_words(text, spanish)
    if overlap:
        # Replace first occurrence of overlap in text with cloze
        escaped_overlap = re.escape(overlap)
        pattern = re.compile(r'\b(' + escaped_overlap + r')\b', re.IGNORECASE)
        match = pattern.search(text)
        if match:
            matched_text = match.group(1)
            card["text"] = pattern.sub(f"{{{{c1::{matched_text}}}}}", text, count=1)
            return True
            
    # Try 2: Extract term from scenario and search in text
    term = extract_core_term(scenario)
    if len(term) > 3:
        # Search for term in text
        escaped_term = re.escape(term)
        pattern = re.compile(r'\b(' + escaped_term + r')\b', re.IGNORECASE)
        match = pattern.search(text)
        if match:
            matched_text = match.group(1)
            card["text"] = pattern.sub(f"{{{{c1::{matched_text}}}}}", text, count=1)
            return True
        # Try substring match if exact word boundary fails
        if term.lower() in text.lower():
            start_idx = text.lower().find(term.lower())
            end_idx = start_idx + len(term)
            matched_text = text[start_idx:end_idx]
            card["text"] = text[:start_idx] + f"{{{{c1::{matched_text}}}}}" + text[end_idx:]
            return True
            
    # Try 3: Fallback — find first word of at least 4 chars in text and wrap it
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
    if words:
        # Exclude common stop words
        stops = {'this', 'that', 'with', 'have', 'your', 'from', 'they', 'were', 'their', 'about', 'will', 'then'}
        for w in words:
            if w.lower() not in stops:
                card["text"] = text.replace(w, f"{{{{c1::{w}}}}}", 1)
                return True
        # If all were stops, just wrap the first word of at least 4 chars
        card["text"] = text.replace(words[0], f"{{{{c1::{words[0]}}}}}", 1)
        return True
        
    return False

def run_repair():
    decks_dir = BASE_DIR / "decks"
    total_repaired = 0
    total_files_updated = 0
    
    for p in decks_dir.glob("**/*.json"):
        if p.name == "index.json":
            continue
            
        with open(p, "r", encoding="utf-8") as f:
            cards = json.load(f)
            
        file_updated = False
        for i, card in enumerate(cards):
            is_valid, _, _ = sanitize_and_validate_card(card)
            if not is_valid:
                if repair_card(card):
                    # Check again
                    is_valid_now, _, errs = sanitize_and_validate_card(card)
                    if is_valid_now:
                        total_repaired += 1
                        file_updated = True
                    else:
                        print(f"  [-] Repair failed for {p.name} card {i}: {errs}")
                        
        if file_updated:
            total_files_updated += 1
            with open(p, "w", encoding="utf-8") as f:
                json.dump(cards, f, indent=2, ensure_ascii=False)
            print(f"[OK] Repaired and saved: {p.name}")
            
    print(f"\n[OK] Repair complete! Total cards repaired: {total_repaired} across {total_files_updated} files.")

if __name__ == "__main__":
    run_repair()
