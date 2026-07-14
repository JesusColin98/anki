import os
import re

memory_dir = r"G:\My Drive\obsidian\Memory"

def scan_files():
    results = {}
    for root, dirs, files in os.walk(memory_dir):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, memory_dir)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    lines = content.splitlines()
                    cards = []
                    in_anki_section = False
                    for i, line in enumerate(lines):
                        stripped = line.strip()
                        if stripped.startswith("## Anki Card") or stripped.startswith("## Anki Flashcards") or stripped.startswith("## Anki"):
                            in_anki_section = True
                            continue
                        
                        if "::" in stripped:
                            cards.append((i+1, stripped))
                        elif stripped.startswith("**") and ("—" in stripped or "-" in stripped or "::" in stripped):
                            cards.append((i+1, stripped))
                        elif stripped.endswith("?") and i < len(lines) - 1 and lines[i+1].strip().startswith("-"):
                            cards.append((i+1, f"{stripped} -> {lines[i+1].strip()}"))
                        elif "{{c" in stripped:
                            cards.append((i+1, stripped))
                    
                    if cards:
                        results[rel_path] = cards
                except Exception as e:
                    print(f"Error reading {rel_path}: {e}")
    return results

if __name__ == "__main__":
    res = scan_files()
    print(f"Found cards in {len(res)} files:")
    for path, cards in sorted(res.items()):
        print(f"\n--- {path} ({len(cards)} items) ---")
        for line_num, card in cards[:10]:
            print(f"Line {line_num}: {card}")
