import os
import re

memory_dir = r"G:\My Drive\obsidian\Memory"

for book in os.listdir(memory_dir):
    book_path = os.path.join(memory_dir, book)
    if not os.path.isdir(book_path):
        continue
    
    count = 0
    examples = []
    
    for file in os.listdir(book_path):
        if file.endswith(".md") and not file.startswith("MOC -"):
            filepath = os.path.join(book_path, file)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                for line in content.splitlines():
                    stripped = line.strip()
                    # Check for - **Term**: Definition
                    match = re.match(r'^(?:-\s+|\*\s+|\d+\.\s+)?\*\*(.*?)\*\*:\s*(.*?)(?:\s*\^.*)?$', stripped)
                    if match:
                        count += 1
                        if len(examples) < 2:
                            examples.append(stripped)
            except Exception as e:
                pass
                
    if count > 0:
        print(f"Book: {book} -> {count} colon-separated terms")
        for ex in examples:
            print(f"  Example: {ex}")
