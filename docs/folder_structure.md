# Folder Structure Documentation

Below is the directory tree of the `anki-tools` project reflecting the modular architecture, template engine, deterministic validator, and MCP server integration:

```text
anki-tools/
├── docs/
│   ├── architecture.md             # Detailed technical architecture & system flow
│   └── folder_structure.md         # Project folder structure documentation
├── decks/                          # Modular subfolder hierarchy (decoupled content)
│   ├── index.json                  # Global index of deck metadata and card counts
│   ├── AI_Learning_Path/           # Machine Learning, LLMs, RAG, and Agent decks
│   ├── Books_Path/                 # Summaries of technical and business books
│   ├── English/                    # Daily life, professional, and phonetics decks
│   ├── French/                     # French A1 and phonetics decks
│   ├── German/                     # German A1 and phonetics decks
│   ├── Italian/                    # Italian A1 and phonetics decks
│   ├── Japanese/                   # Japanese A1 and phonetics decks
│   ├── Korean/                     # Korean A1 and phonetics decks
│   ├── Networking_Security/        # Networking fundamentals and defense decks
│   ├── News_Scraped/               # Web articles scraped by scraper_agent.py
│   ├── Philosophy/                 # Stoicism, classical, and modern philosophy
│   ├── Portuguese/                 # Portuguese A1 and phonetics decks
│   ├── Russian/                    # Russian A1 and phonetics decks
│   ├── Social_Skills/              # Persuasion, active listening, and presence
│   ├── SoftSkills/                 # Communication & soft skills decks
│   ├── Spanish/                    # Spanish A1 and phonetics decks
│   └── Tech_Map_2026/              # Future tech roadmap decks
├── mcp_anki_server.py              # Native MCP Server exposing tools for LLMs/Agents
├── adk_orchestrator.py             # ADK Map-Reduce rolling chunking for books & docs
├── template_engine.py              # Multi-Template Engine implementing 6 Wozniak templates
├── card_validator.py               # Deterministic syntax validator & auto-repair engine
├── scraper_agent.py                # Web scraper & news flashcard generator
├── local_ollama_provider.py        # Ollama local LLM API wrapper (Gemma 2 / Llama 3)
├── migrate_monolith_to_decks.py    # Migration script splitting monolith JSON to decks/
├── anki_db_importer.py             # Recursive sync engine connecting to AnkiConnect
└── clean_anki_duplicates.py        # Duplicate notes cleaner script
```
