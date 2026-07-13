# Folder Structure Documentation

Below is the directory tree of the `anki-tools` project reflecting the decoupled database architecture:

```text
anki-tools/
├── docs/
│   ├── architecture.md          # High-level architecture and system design
│   └── folder_structure.md      # Project folder structure details
├── anki_cards_database.json     # Decoupled JSON file holding all 650 cards
├── anki_db_importer.py          # Primary importer script with two-way sync engine
├── clean_anki_duplicates.py     # Script to identify and remove duplicate cards in Anki
├── add_fast_english_cards.py    # Script appending Fast English connected speech cards
├── add_ai_books_cards.py        # Script appending AI/ML book cards and links
├── ingest_languages.py          # Automated language curriculum and phonetics parser
├── anki_helper.py               # Legacy CLI management helper

├── generate_scenarios.py        # Legacy scenario generator
├── generate_ai_path.py          # Legacy MathJax AI generator
├── generate_books_path.py        # Legacy GDrive books generator
├── add_business_scenarios.py    # Legacy professional roles generator
├── generate_languages_path.py    # Legacy German/French greetings generator
└── generate_philosophy_path.py   # Legacy philosophy MOC generator
```
