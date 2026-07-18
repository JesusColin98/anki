#!/usr/bin/env python3
"""ADK Orchestrator for Long-Form Books, Articles, and Multi-Agent Pipeline.

Applies Map-Reduce sliding window chunking and 5-Archetype procedural
guardrails (Scholar, Analyst, Architect, Producer, Advisor) to extract
high-retention Anki cards using Gemini API.
"""

import json
import hashlib
from pathlib import Path
import sys
from typing import List

# Setup sys.path to find local modules
BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from template_engine import build_card
from scraper_agent import save_cards_to_deck
from gemini_provider import (
    generate_anki_cards_gemini,
    route_chunk_complexity,
    correct_card_with_feedback,
)
from card_validator import sanitize_and_validate_card

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
  # 1. [Scholar Mode]: Log intent and route complexity
  print(f"    [Scholar] Analyzing chunk text (length: {len(chunk_text_data)} characters)...")
  complexity = route_chunk_complexity(chunk_text_data)
  print(f"    [Scholar] Routed chunk complexity as: {complexity}")
  
  # 2. [Analyst & Architect Mode]: Generate via Gemini
  raw_cards = generate_anki_cards_gemini(chunk_text_data, deck_name, complexity=complexity)
  
  # 3. [Producer Mode]: Build and validate with a self-repair loop and fatigue threshold
  validated_cards = []
  for card_data in raw_cards:
      if not isinstance(card_data, dict):
          continue
      
      card_data["deck"] = deck_name
      t_type = card_data.get("template", template_type)
      
      attempts = 0
      max_retries = 3
      success = False
      errors = []
      card_output = {}

      while attempts <= max_retries and not success:
          try:
              # Build and run validator auto-repair inside template engine
              card_output = build_card(t_type, card_data)
              # Check for schema errors
              is_valid, cleaned, errors = sanitize_and_validate_card(card_output)
              if is_valid:
                  card_output = cleaned
                  success = True
              else:
                  raise ValueError(f"Validation errors: {errors}")
          except Exception as e:
              errors = [str(e)]
              attempts += 1
              if attempts <= max_retries:
                  print(f"    [Producer] Attempt {attempts} failed: {errors}. Retrying self-correction...")
                  card_data = correct_card_with_feedback(card_data, errors)
                  card_data["deck"] = deck_name
                  if "template" not in card_data:
                      card_data["template"] = t_type
              else:
                  print(f"    [Producer] Warning: Self-correction fatigue limit reached after {max_retries} attempts.")
                  break

      if success:
          validated_cards.append(card_output)
      else:
          # Graceful degradation fallback
          print("    [Advisor] Graceful degradation: Flagging card with 'low_confidence'.")
          try:
              # Fallback card structure creation
              fallback_card = card_output if card_output else card_data
              # Ensure deck is set
              fallback_card["deck"] = deck_name
              
              # Force nested metadata fields
              if "metadata" not in fallback_card or not isinstance(fallback_card["metadata"], dict):
                  fallback_card["metadata"] = {}
              fallback_card["metadata"]["validation_status"] = "low_confidence"
              tags = fallback_card["metadata"].get("tags", [])
              if "needs_review" not in tags:
                  tags.append("needs_review")
              fallback_card["metadata"]["tags"] = tags

              # Enforce minimal required fields for the builder fallback
              if "content" not in fallback_card or not isinstance(fallback_card["content"], dict):
                  fallback_card["content"] = {
                      "text": fallback_card.get("text", "Fallback Card: Please review details."),
                      "explanation": fallback_card.get("explanation", f"Failed validation errors: {errors}"),
                      "spanish": fallback_card.get("spanish", "Revisar tarjeta.")
                  }

              # Force template to T1_Cloze if missing/unbuildable
              fallback_card["template"] = fallback_card.get("template", "T1_Cloze")

              validated_cards.append(fallback_card)
              
              # Write failed payload to scratch for troubleshooting
              card_id = fallback_card.get("id", hashlib.sha256(str(card_data).encode('utf-8')).hexdigest()[:16])
              scratch_dir = BASE_DIR / "scratch" / "troubleshooting"
              scratch_dir.mkdir(parents=True, exist_ok=True)
              trouble_file = scratch_dir / f"failed_card_{card_id}.json"
              with open(trouble_file, "w", encoding="utf-8") as f:
                  json.dump({
                      "original_data": card_data,
                      "repaired_state": fallback_card,
                      "errors": errors
                  }, f, indent=2, ensure_ascii=False)
          except Exception as degrade_err:
              print(f"    [-] Failed to perform graceful degradation: {degrade_err}", file=sys.stderr)
          
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
      sample_long_text, "Spaced Repetition Guide", "06_Business_and_Productivity::Learning_and_Memory::Methodology::Spaced_Repetition_Research"
  )
  print(json.dumps(result, indent=2))
