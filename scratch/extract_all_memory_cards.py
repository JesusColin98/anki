import os
import re
import json
import sys

memory_dir = r"G:\My Drive\obsidian\Memory"
output_file = r"C:\Users\jesus\.gemini\antigravity\scratch\anki-tools\scratch\extracted_memory_cards.json"

def clean_text(text):
    text = re.sub(r'\^[a-zA-Z0-9\-]+$', '', text)
    return text.strip()

def parse_md_file(filepath, book_name):
    cards = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}", flush=True)
        return []
    
    lines = content.splitlines()
    current_header = ""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## "):
            current_header = stripped[3:].strip()
            continue
        
        if not stripped:
            continue
            
        if "{{c" in stripped:
            cards.append({
                "type": "cloze",
                "line_num": i + 1,
                "header": current_header,
                "text": clean_text(stripped)
            })
            continue
            
        # Use our super-robust regex for bold term/definition or question/answer
        match = re.match(r'^(?:-\s+|\*\s+|\d+\.\s+)?\*\*(.*?)\*\*[:\s—–-]*\s*(.*)$', stripped)
        if match:
            term = match.group(1).strip()
            definition = match.group(2).strip()
            
            # Clean trailing colon from term if it was inside bolding
            if term.endswith(":"):
                term = term[:-1].strip()
                
            # Filter out non-card navigation or links
            term_lower = term.lower()
            if any(x in term_lower for x in ["back to moc", "next step", "previous chapter", "next chapter", "summary tracker", "moc -"]):
                continue
            if not definition:
                continue
            if definition.startswith("[[") and definition.endswith("]]"):
                continue
                
            # Remove block id from definition
            definition = clean_text(definition)
            
            # If definition is also bolded, it might be a QA bold card
            if definition.startswith("**") and definition.endswith("**"):
                inner_def = definition[2:-2].strip()
                cards.append({
                    "type": "qa_bold",
                    "line_num": i + 1,
                    "header": current_header,
                    "question": term,
                    "answer": inner_def
                })
            else:
                cards.append({
                    "type": "term_def",
                    "line_num": i + 1,
                    "header": current_header,
                    "term": term,
                    "definition": definition
                })
            continue
            
        if "::" in stripped and not stripped.startswith("{"):
            parts = stripped.split("::", 1)
            q = clean_text(parts[0])
            a = clean_text(parts[1])
            if q and a:
                cards.append({
                    "type": "double_colon",
                    "line_num": i + 1,
                    "header": current_header,
                    "question": q,
                    "answer": a
                })
            continue

    return cards

def scan_all():
    print("Starting scan...", flush=True)
    all_books_cards = {}
    if not os.path.exists(memory_dir):
        print(f"Error: {memory_dir} does not exist", flush=True)
        return
        
    folders = os.listdir(memory_dir)
    print(f"Found {len(folders)} folders to scan.", flush=True)
    
    for idx, book_folder in enumerate(folders):
        book_path = os.path.join(memory_dir, book_folder)
        if not os.path.isdir(book_path):
            continue
        
        print(f"[{idx+1}/{len(folders)}] Scanning folder: {book_folder}...", flush=True)
        all_books_cards[book_folder] = []
        
        try:
            files = os.listdir(book_path)
            for file in files:
                if file.endswith(".md") and not file.startswith("MOC -"):
                    filepath = os.path.join(book_path, file)
                    file_cards = parse_md_file(filepath, book_folder)
                    if file_cards:
                        all_books_cards[book_folder].append({
                            "file": file,
                            "cards": file_cards
                        })
        except Exception as e:
            print(f"Error scanning folder {book_folder}: {e}", flush=True)
                    
    # Remove books with no cards
    all_books_cards = {k: v for k, v in all_books_cards.items() if v}
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_books_cards, f, indent=2, ensure_ascii=False)
        
    print(f"Extraction complete. Saved to {output_file}", flush=True)
    
if __name__ == "__main__":
    scan_all()
