import os

path = r"G:\My Drive\obsidian\Memory\Ultralearning\Chapter 8 - Principle 5 - Retrieval.md"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    for i, line in enumerate(lines[:20]):
        print(f"Line {i+1}: {repr(line)}")
else:
    print("Path does not exist")
