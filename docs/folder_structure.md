# Folder Structure Documentation

Below is the directory tree of the `anki-tools` project reflecting the modular architecture, template engine, deterministic validator, and MCP server integration:

```text
anki-tools/
├── docs/
│   ├── architecture.md             # Detailed technical architecture & system flow
│   ├── card_quality_and_templates_guide.md # Guide on card quality, prompt patterns, & templates
│   └── folder_structure.md         # Project folder structure documentation
├── decks/                          # 4-Level Deep Deck Hierarchy (6 Scalable Pillars)
│   ├── index.json                  # Global index of deck metadata and card counts
│   ├── 01_Cloud_and_Infrastructure/ # Networking, cybersecurity, cloud, & systems engineering
│   ├── 02_AI_and_Data_Science/     # Classical ML, LLMs, agents, RAG, MLOps, & data science
│   ├── 03_Languages/               # English, Spanish, Asian/European languages & news
│   │   └── English/
│   │       ├── Learning_Paths/     # Consolidated 4-level English learning paths
│   │       │   ├── 01_Daily_and_Social/
│   │       │   ├── 02_Workplace_and_Service/
│   │       │   ├── 03_Interview_and_Career/
│   │       │   └── 04_Academic_and_Health/
│   │       ├── Phonetics/          # Accent, pronunciation, and connected speech decks
│   │       ├── 08_Real_Scenario_Expansion/ # Raw scenario expansion files
│   │       └── Variant_Pipeline/   # Holds pipeline configuration manifest.json
│   ├── 04_Social_and_Humanities/   # Philosophy, history, sociology, & psychology
│   ├── 05_Soft_Skills_and_Leadership/ # Persuasion, active listening, etiquette, & leadership
│   └── 06_Business_and_Productivity/ # Business strategy, productivity, & learning methods
├── migrate_to_4level_hierarchy.py  # Script migrating decks to 4-level deep hierarchy
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
