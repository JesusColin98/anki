import json

with open("scratch/extracted_memory_cards.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("SUMMARY OF EXTRACTED CARDS BY BOOK:")
total = 0
for book, file_entries in data.items():
    book_total = 0
    for entry in file_entries:
        book_total += len(entry["cards"])
    print(f"- {book}: {book_total} cards across {len(file_entries)} files")
    total += book_total
print(f"Grand Total: {total} cards")
