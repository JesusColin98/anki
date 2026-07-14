---
name: anki_adk_mastery
description: Workspace skill for creating, validating, cleaning, and syncing Anki flashcards using Gemini and the centralized ADK hub.
---

# Anki ADK Mastery Skill

This skill equips the agent with direct knowledge on how to manage, validate, clean, and sync Anki decks in the `anki-tools` project, as well as how to trigger Gemini-based article scraping and card generation.

---

## 1. Pillars and Hierarchy Structure

All decks in this repository are divided into **6 scalable learning pillars** and must maintain exactly **4 levels of deck depth** (`Pillar::Category::Subcategory::DeckName`):

1. **`01_Cloud_and_Infrastructure`**: Networking, Cybersecurity, Cloud services, and Systems Engineering.
2. **`02_AI_and_Data_Science`**: Classical ML, LLM systems, Agentic frameworks, RAG, and MLOps.
3. **`03_Languages`**: Language learning (German, French, English, etc.) and connected speech phonetics.
4. **`04_Social_and_Humanities`**: Philosophy, history, and conversational psychology.
5. **`05_Soft_Skills_and_Leadership`**: Communication, presence, active listening, and support excellence.
6. **`06_Business_and_Productivity`**: Business strategy, productivity books, and learning techniques.

---

## 2. Centralized Operations CLI (`anki_adk_hub.py`)

The codebase exposes all operations under a single, unified CLI hub script:

```bash
python anki_adk_hub.py <command> [args]
```

### Subcommands:

- **`validate`**: Enforces the 4-level deep directory structure and syntax validation (checks MathJax delimiters, balanced Cloze deletions, and corrects malformed Mermaid charts).
  ```bash
  python anki_adk_hub.py validate
  ```
- **`sync`**: Performs a 2-way synchronization, loading cards from all JSON files in the `decks/` tree and importing them into Anki Desktop via AnkiConnect (port 8765).
  ```bash
  python anki_adk_hub.py sync
  ```
- **`clean`**: Identifies and deletes duplicate notes of the `Engaging_Cloze_Model` in Anki Desktop.
  ```bash
  python anki_adk_hub.py clean
  ```
- **`audit`**: Lists all decks with 0 notes currently loaded in Anki Desktop.
  ```bash
  python anki_adk_hub.py audit
  ```
- **`delete-legacy`**: Deletes empty legacy decks from previous versions to clean up your Anki workspace.
  ```bash
  python anki_adk_hub.py delete-legacy
  ```
- **`scrape-ingest`**: Scrapes a web page URL, processes its paragraphs through a Map-Reduce rolling window, invokes Gemini API to generate atomic, high-quality cards, and saves them.
  ```bash
  python anki_adk_hub.py scrape-ingest <URL> <DeckName>
  ```

---

## 3. Card Quality Standards

Every generated card must pass these strict criteria:
- **`scenario`**: Short category prefix with a descriptive emoji (e.g. `Cloud Security 🔒: IAM Authorization`).
- **`text`**: Exactly one balanced cloze tag (e.g. `{{c1::concept}}`). No unclosed brackets.
- **`explanation`**: A thorough breakdown of the "why" and context (minimum 20 characters).
- **`usage`**: Structured HTML examples or code snippets (`<ul><li>...</li></ul>`).
- **`spanish`**: A natural and accurate Spanish translation of the text and context.
