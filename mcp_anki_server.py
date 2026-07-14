#!/usr/bin/env python3
"""Native MCP (Model Context Protocol) Server Engine for Anki App Wrapper.

Exposes native tools for AI Agents and LLMs to inspect, edit, scrape, and sync
Anki decks by delegating to the centralized anki_adk_hub.
"""

import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).parent.resolve()
DECKS_DIR = BASE_DIR / "decks"

# Ensure root is in sys.path
sys.path.insert(0, str(BASE_DIR))
import anki_adk_hub
from scraper_agent import save_cards_to_deck
from template_engine import build_card

def mcp_anki_list_decks() -> dict:
    """Lists all available decks and subdecks with card counts."""
    return anki_adk_hub.anki_invoke('deckNames')

def mcp_anki_read_deck(deck_name: str) -> list:
    """Reads all cards belonging to a specific subdeck."""
    rel_path = deck_name.replace("::", "/") + ".json"
    target_file = DECKS_DIR / rel_path
    if not target_file.exists():
        return []

    with open(target_file, "r", encoding="utf-8") as f:
        return json.load(f)

def mcp_anki_create_card(template_type: str, data: dict) -> dict:
    """Creates a single Anki card using template_engine and saves it to its deck."""
    card = build_card(template_type, data)
    save_cards_to_deck([card], data["deck"])
    anki_adk_hub.regenerate_index()
    return {"status": "SUCCESS", "created_card": card}

def mcp_anki_scrape_and_generate(url: str, deck_name: str) -> dict:
    """Scrapes a URL, extracts facts via Gemini LLM pipeline, and saves cards."""
    try:
        anki_adk_hub.cmd_scrape_ingest(url, deck_name)
        return {"status": "SUCCESS", "message": f"Successfully ingested {url} into {deck_name}."}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

def mcp_anki_sync() -> dict:
    """Triggers 2-way sync with AnkiConnect Desktop."""
    try:
        anki_adk_hub.cmd_sync()
        return {"status": "SUCCESS", "message": "Synced decks tree with Anki Desktop."}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

def mcp_anki_validate() -> dict:
    """Validates the decks hierarchy and card syntax."""
    try:
        success = anki_adk_hub.cmd_validate()
        return {"status": "SUCCESS" if success else "FAILED"}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

def mcp_anki_clean_duplicates() -> dict:
    """Cleans duplicate notes in Anki Connect."""
    try:
        anki_adk_hub.cmd_clean()
        return {"status": "SUCCESS", "message": "Duplicate cleanup complete."}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

def main():
    """CLI Command Dispatcher for MCP Tool Invocation."""
    if len(sys.argv) < 2:
        print("Anki MCP Server CLI")
        print("Commands: list_decks | read_deck | scrape | sync | validate | clean")
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "list_decks":
        print(json.dumps(mcp_anki_list_decks(), indent=2, ensure_ascii=False))
    elif cmd == "read_deck" and len(sys.argv) > 2:
        print(json.dumps(mcp_anki_read_deck(sys.argv[2]), indent=2, ensure_ascii=False))
    elif cmd == "scrape" and len(sys.argv) > 3:
        print(json.dumps(mcp_anki_scrape_and_generate(sys.argv[2], sys.argv[3]), indent=2))
    elif cmd == "sync":
        print(json.dumps(mcp_anki_sync(), indent=2))
    elif cmd == "validate":
        print(json.dumps(mcp_anki_validate(), indent=2))
    elif cmd == "clean":
        print(json.dumps(mcp_anki_clean_duplicates(), indent=2))
    else:
        print(f"Unknown or incomplete command: {cmd}")

if __name__ == "__main__":
    main()
