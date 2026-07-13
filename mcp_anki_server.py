#!/usr/bin/env python3
"""Native MCP (Model Context Protocol) Server Engine for Anki App Wrapper.

Exposes native tools for AI Agents and LLMs to inspect, edit, scrape, and sync
Anki decks:
- mcp_anki_list_decks
- mcp_anki_read_deck
- mcp_anki_scrape_and_generate
- mcp_anki_create_card
- mcp_anki_sync
"""

import json
from pathlib import Path
import sys
from adk_orchestrator import orchestrate_document
from anki_db_importer import import_database, load_all_cards
from scraper_agent import save_cards_to_deck, scrape_article
from template_engine import TEMPLATES, build_card

BASE_DIR = Path(__file__).parent.resolve()
DECKS_DIR = BASE_DIR / "decks"


def mcp_anki_list_decks() -> dict:
  """Lists all available decks and subdecks with card counts."""
  index_file = DECKS_DIR / "index.json"
  if index_file.exists():
    with open(index_file, "r", encoding="utf-8") as f:
      return json.load(f)

  # Fallback: scan decks directory
  decks = []
  total = 0
  for p in DECKS_DIR.glob("**/*.json"):
    if p.name == "index.json":
      continue
    with open(p, "r", encoding="utf-8") as f:
      cards = json.load(f)
      count = len(cards)
      total += count
      deck_name = str(p.relative_to(DECKS_DIR).with_suffix("")).replace(
          "/", "::"
      )
      decks.append(
          {"deck": deck_name, "path": str(p), "cards_count": count}
      )

  return {"total_cards": total, "total_decks": len(decks), "decks": decks}


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
  return {"status": "SUCCESS", "created_card": card}


def mcp_anki_scrape_and_generate(
    url: str, deck_name: str = "News_Scraped::General"
) -> dict:
  """Scrapes a URL, extracts facts via ADK pipeline, and saves cards."""
  article = scrape_article(url)
  result = orchestrate_document(
      article["full_text"], article["title"], deck_name
  )
  return result


def mcp_anki_sync() -> dict:
  """Triggers 2-way sync with AnkiConnect Desktop."""
  try:
    import_database()
    return {"status": "SUCCESS", "message": "Synced decks tree with Anki Desktop."}
  except Exception as e:
    return {"status": "ERROR", "error": str(e)}


def main():
  """CLI Command Dispatcher for MCP Tool Invocation."""
  if len(sys.argv) < 2:
    print("Anki MCP Server CLI")
    print("Commands: list_decks | read_deck | scrape | sync")
    sys.exit(0)

  cmd = sys.argv[1]
  if cmd == "list_decks":
    print(json.dumps(mcp_anki_list_decks(), indent=2, ensure_ascii=False))
  elif cmd == "read_deck" and len(sys.argv) > 2:
    print(json.dumps(mcp_anki_read_deck(sys.argv[2]), indent=2, ensure_ascii=False))
  elif cmd == "scrape" and len(sys.argv) > 2:
    deck = sys.argv[3] if len(sys.argv) > 3 else "News_Scraped::General"
    print(json.dumps(mcp_anki_scrape_and_generate(sys.argv[2], deck), indent=2))
  elif cmd == "sync":
    print(json.dumps(mcp_anki_sync(), indent=2))
  else:
    print(f"Unknown or incomplete command: {cmd}")


if __name__ == "__main__":
  main()
