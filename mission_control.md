---
project: "anki-4level-migration"
active_stage: "REVIEW"
progress: 20
---

# Mission Control: Anki 4-Level Deep Deck Hierarchy Migration

## Project Overview & DoD
- **Goal**: Reorganize 97 subdeck JSON files into a 4-level deep directory hierarchy under 5 main pillars. Update `anki_db_importer.py` for recursive scanning and regenerate `decks/index.json`.
- **Definition of Done (DoD)**:
  1. Script `migrate_to_4level_hierarchy.py` created and executed successfully, placing all subdecks into 4-level deep pillar directories.
  2. `anki_db_importer.py` updated to support arbitrary recursive directory scanning for JSON deck files.
  3. `decks/index.json` regenerated and verified reflecting the 4-level hierarchy.
  4. Unit/validation tests pass cleanly.

## Cognitive Budgeting
- **Tier**: Tier 2 (\tau=Medium, Standard System 2) - Multi-file refactoring & hierarchy migration.

## Active Stage & Checklist
- [ ] Step 1: `[Scholar Mode]` - Analyze existing `decks/` structure and `anki_db_importer.py` / `migrate_monolith_to_decks.py`.
- [ ] Step 2: `[Analyst Mode]` - Design the 4-level hierarchy structure and recursive scanner logic for `anki_db_importer.py`.
- [ ] Step 3: `[Architect Mode]` - Map the 5 pillars and directory paths for `migrate_to_4level_hierarchy.py` and outline detailed migration plan.
- [ ] Step 4: `[Producer Mode]` - Implement `migrate_to_4level_hierarchy.py`, update `anki_db_importer.py`, execute migration, and regenerate `decks/index.json`.
- [x] 🟢 Step 5: `[Advisor Mode]` - Validate whole hierarchy, test import functionality, run unit tests, and verify DoD.

## Diagnostic Log & Evidence
- *Init*: Initialized workspace at `/tmp/anki_repo`.
