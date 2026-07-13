import os

root_dir = r"G:\My Drive\ocularis\languages"

md_files = []
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".md"):
            full_path = os.path.join(root, file)
            md_files.append(full_path)

print(f"Total markdown files found: {len(md_files)}")
print("\nFirst 20 files:")
for f in md_files[:20]:
    print(f.replace(root_dir, ""))
