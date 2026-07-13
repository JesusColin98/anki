# Workspace Customization Rules: Anki ADK & 4-Level Migration

These rules are project-scoped for the `anki-tools` workspace and must be adhered to during all agent tasks (code refactoring, card generation, and system operations).

---

## 1. The 5-Archetype Procedural Workflow
When tackling any feature addition, refactoring, or card generation task, structure your thinking and execution using the following sequential modes:

1. **[Scholar Mode] (Context & Architecture Analysis)**
   - Prioritize reading existing documentation under `/docs` and inspecting schemas.
   - Run diagnostics first before writing any code. Do not proceed without context.
2. **[Analyst Mode] (Atomicity & Minimum Information)**
   - Enforce Wozniak's Minimum Information Principle: **1 fact per card**.
   - Ensure Cloze deletions (`{{c1::...}}`) are balanced, unambiguous, and target the key concept only.
3. **[Architect Mode] (Hierarchical Structural Integrity)**
   - Ensure all cards are mapped to one of the **6 Pillars**:
     - `01_Cloud_and_Infrastructure`
     - `02_AI_and_Data_Science`
     - `03_Languages`
     - `04_Social_and_Humanities`
     - `05_Soft_Skills_and_Leadership`
     - `06_Business_and_Productivity`
   - Maintain exactly **4 levels of deck depth** (e.g., `Pillar::Category::Subcategory::DeckName`).
   - Choose the appropriate template (**T1_Cloze** to **T9_ContrastivePhonetics**) based on the use case.
4. **[Producer Mode] (Implementation & Auto-Validation)**
   - Implement clean, modular scripts.
   - **Mandatory Rule**: Always validate new cards using the `card_validator.py` sanitation pipeline before saving them to `decks/`.
5. **[Advisor Mode] (Quality Verification)**
   - Run verification scripts (such as `validate_deck_hierarchy.py` and unit tests under `tests/`) to ensure no syntax or structural errors exist.

---

## 2. Card Quality Standards & Syntax Sanitization
Every generated card must pass these strict criteria:
- **`scenario`**: Must be descriptive, prefixed with category + emoji (e.g. `Fast English: Flap T ⚡`).
- **`text`**: Must contain exactly one balanced cloze tag (e.g. `{{c1::concept}}`). No unclosed brackets.
- **`explanation`**: Must provide a clear "Why" and intuitive conceptual breakdown (minimum 20 characters).
- **`usage`**: Must contain structured HTML examples (e.g. `<ul><li>...</li></ul>`).
- **`spanish`**: Must provide a natural and accurate Spanish translation of the text and context.
- **Mermaid Diagrams**: Arrows must be valid (`-->` instead of `->`), and node labels containing special characters must be double-quoted.
- **MathJax Delimiters**: Ensure blocks use `\[...\]` and inline formulas use `\(...\)` with balanced opening/closing tags.

---

## 3. Operations & Index Maintenance
- **Two-Way Synchronization**: When importing or syncing to Anki, use the case-insensitive sync engine in `anki_db_importer.py` to prevent duplicate creations and update existing records in-place.
- **Index Generation**: After any deck modification or addition, always run migration and deck verification tools to regenerate `decks/index.json`.
- **Exclusively JSON Content**: Always write card/learning content directly to the JSON deck files under `decks/...`. Never hardcode card lists or study materials inside Python scripts (e.g. `add_fast_english_cards.py` or `add_english_scenario_cards.py` are deprecated patterns). Python scripts must only contain logic, whereas data must reside exclusively in the JSON files.
