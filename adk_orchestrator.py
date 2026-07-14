#!/usr/bin/env python3
"""ADK Orchestrator for Long-Form Books, Articles, and Multi-Agent Pipeline.

Applies Map-Reduce sliding window chunking and 5-Archetype procedural
guardrails (Scholar, Analyst, Architect, Producer, Advisor) to extract
high-retention Anki cards using Gemini API.
"""

import json
from pathlib import Path
import sys
from typing import List

# Setup sys.path to find local modules
BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from template_engine import build_card
from scraper_agent import save_cards_to_deck
from gemini_provider import generate_anki_cards_gemini

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
  """Applies 5-Archetype LLM processing to extract atomic cards from a chunk."""
  # 1. [Scholar Mode]: Log intent
  print(f"    [Scholar] Analyzing chunk text (length: {len(chunk_text_data)} characters)...")
  
  # 2. [Analyst & Architect Mode]: Generate via Gemini (which handles Wozniak atomicity constraints)
  raw_cards = generate_anki_cards_gemini(chunk_text_data, deck_name)
  
  # 3. [Producer Mode]: Build and validate using template_engine / validator
  validated_cards = []
  for card_data in raw_cards:
      try:
          # Verify card data contains deck
          card_data["deck"] = deck_name
          # Build and validate
          card = build_card(template_type, card_data)
          validated_cards.append(card)
      except Exception as e:
          print(f"    [-] Card build error in Producer mode: {e}", file=sys.stderr)
          
  # 4. [Advisor Mode]: Return validated cards
  print(f"    [Advisor] Generated {len(validated_cards)} validated cards from chunk.")
  return validated_cards


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
      sample_long_text, "Spaced Repetition Guide", "06_Business_and_Productivity::Productivity::Learning::Spaced_Repetition_Research"
  )
  print(json.dumps(result, indent=2))
