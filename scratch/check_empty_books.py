import os

memory_dir = r"G:\My Drive\obsidian\Memory"
empty_books = [
    "A Mind For Numbers",
    "Become a SuperLearner",
    "Building a Second Brain",
    "Fanatical Prospecting",
    "Memory Craft",
    "Moonwalking with Einstein",
    "The Memory Book",
    "Tiny Habits",
    "Ultralearning",
    "Unlimited Memory",
    "The Art Of Memory"
]

for book in empty_books:
    book_path = os.path.join(memory_dir, book)
    if not os.path.exists(book_path):
        continue
    print(f"\n===== BOOK: {book} =====")
    files = [f for f in os.listdir(book_path) if f.endswith(".md")]
    print(f"Files: {len(files)}")
    
    # Check if there are any files with "Anki" in them or headings
    headings_with_anki = []
    lines_with_bold_dash = []
    lines_with_double_colon = []
    
    for file in files:
        filepath = os.path.join(book_path, file)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.splitlines()
            for i, line in enumerate(lines):
                s = line.strip()
                if "##" in s and ("Anki" in s or "Takeaway" in s or "Key" in s):
                    headings_with_anki.append((file, i+1, s))
                if "**" in s and ("—" in s or " - " in s):
                    lines_with_bold_dash.append((file, i+1, s))
                if "::" in s and not s.startswith("{"):
                    lines_with_double_colon.append((file, i+1, s))
        except Exception as e:
            print(f"Error {file}: {e}")
            
    print(f"Headings like Anki/Key: {len(headings_with_anki)}")
    for item in headings_with_anki[:3]:
        print(f"  {item[0]} L{item[1]}: {item[2]}")
        
    print(f"Lines with **Term** - Def: {len(lines_with_bold_dash)}")
    for item in lines_with_bold_dash[:3]:
        print(f"  {item[0]} L{item[1]}: {item[2]}")
        
    print(f"Lines with ::: {len(lines_with_double_colon)}")
    for item in lines_with_double_colon[:3]:
        print(f"  {item[0]} L{item[1]}: {item[2]}")
