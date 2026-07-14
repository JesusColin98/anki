with open(r"G:\My Drive\obsidian\Memory\A Mind For Numbers\Chapter 1 - Open the Door.md", "rb") as f:
    content = f.read()

# Let's find the line with "Self-Portrait Barrier"
for line in content.splitlines():
    if b"Self-Portrait" in line:
        print("Raw bytes:", line)
        # Decode as utf-8, ignore errors, and print characters and their code points
        decoded = line.decode("utf-8", errors="replace")
        print("Decoded (UTF-8):", decoded)
        for char in decoded:
            print(f"Char: {repr(char)}, Code Point: {ord(char)}")
