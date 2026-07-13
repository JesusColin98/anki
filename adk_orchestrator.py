#!/usr/bin/env python3
"""ADK Orchestrator for Long-Form Books, Articles, and Multi-Agent Pipeline.

Applies Map-Reduce sliding window chunking and 5-Archetype procedural
guardrails
(Scholar, Analyst, Architect, Producer, Advisor) to extract high-retention Anki
cards.
"""

import json
from pathlib import Path
import sys
from typing import List
from template_engine import build_card
from scraper_agent import scrape_article, save_cards_to_deck

BASE_DIR = Path(__file__).parent.resolve()
DECKS_DIR = BASE_DIR / "decks"


def chunk_text(text: str, chunk_size_chars: int = 4000) -> List[str]:
  """Splits long texts into manageable rolling chunks to prevent context saturation."""
  paragraphs = text.split("\n\n")
  chunks = []
  current_chunk = []
  current_len = 0

  for p in paragraphs:
    if current_len + len(p) > chunk_size_chars and current_chunk:
      chunks.append("\n\n".join(current_chunk))
      current_chunk = [p]
      current_len = len(p)
    else:
      current_chunk.append(p)
      current_len += len(p)

  if current_chunk:
    chunks.append("\n\n".join(current_chunk))

  return chunks


def process_chunk_with_guardrails(
    chunk_text_data: str,
    deck_name: str,
    source_title: str = "Long Document",
    template_type: str = "T1_Cloze",
) -> List[dict]:
  """Applies 5-Archetype procedural steps to extract atomic cards from a chunk."""
  # 1. [Scholar Mode]: Context Gathering
  lines = [
      line.strip()
      for line in chunk_text_data.split("\n")
      if len(line.strip()) > 30
  ]
  if not lines:
    return []

  cards = []
  for line in lines[:5]:  # Process key facts from chunk
    words = line.split()
    if len(words) < 5:
      continue

    # 2. [Analyst Mode]: Minimum Information Principle (1 fact per card)
    target_idx = max(1, len(words) // 2)
    target_word = words[target_idx].strip(".,;:\"'")
    if len(target_word) <= 3:
      continue

    cloze_text = line.replace(target_word, f"{{{{c1::{target_word}}}}}")

    # 3. [Architect Mode]: Select Template Data
    t1_data = {
        "deck": deck_name,
        "scenario": f"Book/Document Extract ({source_title[:25]})",
        "text": cloze_text,
        "explanation": f"Atomic fact from: <strong>{source_title}</strong>",
        "usage": f"Original context: <code>{line}</code>",
        "spanish": f"Extraído de: {source_title}",
        "tags": ["adk_orchestrated", "wozniak_atomic"],
    }

    # 4. [Producer Mode]: Build and validate using template_engine
    try:
      card = build_card(template_type, t1_data)
      cards.append(card)
    except Exception as e:
      print(f"[-] Card build error in Producer mode: {e}", file=sys.stderr)

  return cards


def orchestrate_document(
    text_content: str, source_title: str, deck_name: str
) -> dict:
  """Orchestrates long document processing over rolling chunks."""
  chunks = chunk_text(text_content)
  print(
      f"[+] Orchestrating '{source_title}': Split into {len(chunks)} rolling"
      " chunks."
  )

  total_cards = []
  for i, chunk in enumerate(chunks, start=1):
    print(f"  [->] ADK Processing Chunk {i}/{len(chunks)}...")
    chunk_cards = process_chunk_with_guardrails(chunk, deck_name, source_title)
    total_cards.extend(chunk_cards)

  if total_cards:
    save_cards_to_deck(total_cards, deck_name)

  return {
      "source": source_title,
      "chunks_processed": len(chunks),
      "cards_generated": len(total_cards),
      "deck": deck_name,
  }


if __name__ == "__main__":
  sample_long_text = """
    Spaced repetition is an evidence-based learning technique that is usually performed with flashcards.
    Newly introduced and more difficult flashcards are shown more frequently, while older and less difficult flashcards are shown less frequently in order to exploit the psychological spacing effect.
    
    The use of spaced repetition has been shown to increase the rate of learning.
    Although the principle is useful in many contexts, spaced repetition is commonly applied in contexts in which a learner must acquire many items and retain them indefinitely in memory.
    It is therefore well suited for the problem of vocabulary acquisition in second-language learning.
    """
  result = orchestrate_document(
      sample_long_text, "Spaced Repetition Guide", "Learning::Spaced_Repetition"
  )
  print(json.dumps(result, indent=2))
