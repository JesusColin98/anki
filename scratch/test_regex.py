import os
import re

path = r"G:\My Drive\obsidian\Memory\Ultralearning\Chapter 8 - Principle 5 - Retrieval.md"
with open(path, "r", encoding="utf-8") as f:
    lines = f.read().splitlines()

for i, line in enumerate(lines):
    stripped = line.strip()
    match = re.match(r'^(?:-\s+|\*\s+|\d+\.\s+)?\*\*(.*?)\*\*:\s*(.*?)(?:\s*\^.*)?$', stripped)
    if match:
        print(f"L{i+1}: {stripped}")
        print(f"  Group 1: {match.group(1)}")
        print(f"  Group 2: {match.group(2)}")
