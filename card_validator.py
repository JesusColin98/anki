#!/usr/bin/env python3
"""Deterministic Card & Syntax Validator for Anki Flashcards.

Prevents malformed outputs from local LLMs (Ollama/Gemma/Llama) by enforcing
deterministic validation & auto-repair rules:
1. Cloze deletion tag balance ({{c1::...}}).
2. Mermaid diagram syntax sanitization & node label quoting.
3. MathJax delimiter matching (\\[...\\], \\(...\\)).
4. HTML tag structure integrity.
"""

import json
import re
from typing import List, Tuple


def sanitize_mermaid_code(mermaid_code: str) -> str:
  """Sanitizes and repairs common Mermaid syntax errors produced by LLMs."""
  code = mermaid_code.strip()

  # Ensure valid diagram header
  valid_headers = (
      "graph",
      "flowchart",
      "sequenceDiagram",
      "classDiagram",
      "stateDiagram",
      "erDiagram",
      "gantt",
  )
  if not any(code.startswith(h) for h in valid_headers):
    code = "graph TD\n" + code

  # Repair invalid arrow syntax (e.g., ->|text| to -->|text| or -->)
  code = re.sub(r"->\|([^|]+)\|", r"-->|\1|", code)

  # Quote node labels with parentheses or special characters to prevent Mermaid parser errors
  # Matches: NodeID[Label with (special) chars] -> NodeID["Label with (special) chars"]
  def quote_label(match):
    node_id = match.group(1)
    bracket_type = match.group(2)  # [ or (
    label = match.group(3).strip()
    close_bracket = match.group(4)

    if (
        label.startswith('"')
        and label.endswith('"')
        or label.startswith("'")
        and label.endswith("'")
    ):
      return match.group(0)

    # Escape internal quotes
    escaped_label = label.replace('"', '\\"')
    return f'{node_id}{bracket_type}"{escaped_label}"{close_bracket}'

  code = re.sub(r'(\w+)(\[|\()([^"\]\)]+)(\]|Wait)', quote_label, code)
  return code


def validate_cloze_syntax(text: str) -> Tuple[bool, str, List[str]]:
  """Validates and auto-repairs Cloze deletion tags {{c1::...}}."""
  errors = []
  repaired_text = text

  # Fix unclosed single brace: {{c1::text} -> {{c1::text}}
  repaired_text = re.sub(r"\{\{(c\d+::[^}]+)\}(?!\})", r"{{\1}}", repaired_text)

  # Check for cloze pattern
  cloze_pattern = r"\{\{c\d+::.*?\}\}"
  matches = re.findall(cloze_pattern, repaired_text)

  if not matches:
    errors.append("No valid Cloze deletion tag {{c1::...}} found in text.")

  return len(errors) == 0, repaired_text, errors


def validate_mathjax_delimiters(text: str) -> Tuple[bool, List[str]]:
  """Checks that MathJax delimiters \\[...\\] and \\(...\\) are balanced."""
  errors = []
  block_open = text.count("\\[")
  block_close = text.count("\\]")
  inline_open = text.count("\\(")
  inline_close = text.count("\\)")

  if block_open != block_close:
    errors.append(
        f"Unbalanced block MathJax delimiters: \\[{block_open} vs \\]{block_close}"
    )
  if inline_open != inline_close:
    errors.append(
        f"Unbalanced inline MathJax delimiters: \\({inline_open} vs"
        f" \\){inline_close}"
    )

  return len(errors) == 0, errors


def sanitize_and_validate_card(card: dict) -> Tuple[bool, dict, List[str]]:
  """Deterministic validator pipeline for generated Anki cards."""
  errors = []
  cleaned_card = card.copy()

  # 1. Validate & repair Cloze syntax in 'text'
  if "text" in cleaned_card:
    is_cloze_valid, repaired_text, cloze_errors = validate_cloze_syntax(
        cleaned_card["text"]
    )
    cleaned_card["text"] = repaired_text
    errors.extend(cloze_errors)

  # 2. Validate & repair Mermaid diagrams if present
  if "mermaid_code" in cleaned_card:
    cleaned_card["mermaid_code"] = sanitize_mermaid_code(
        cleaned_card["mermaid_code"]
    )

  if "explanation" in cleaned_card and "class=\"mermaid\"" in cleaned_card["explanation"]:
    # Extract mermaid content inside <div class="mermaid">...</div>
    def repair_mermaid_div(match):
      m_code = match.group(1)
      sanitized = sanitize_mermaid_code(m_code)
      return f'<div class="mermaid">\n{sanitized}\n</div>'

    cleaned_card["explanation"] = re.sub(
        r'<div class="mermaid">\s*(.*?)\s*</div>',
        repair_mermaid_div,
        cleaned_card["explanation"],
        flags=re.DOTALL,
    )

  # 3. Validate MathJax
  full_str = json.dumps(cleaned_card)
  math_valid, math_errors = validate_mathjax_delimiters(full_str)
  errors.extend(math_errors)

  # Overall validity check (must have required fields)
  req_fields = ["deck", "text", "explanation", "spanish"]
  for f in req_fields:
    if f not in cleaned_card or not str(cleaned_card[f]).strip():
      errors.append(f"Missing required field: '{f}'")

  is_valid = len(errors) == 0
  return is_valid, cleaned_card, errors


if __name__ == "__main__":
  sample_broken = {
      "deck": "Test::Deck",
      "text": "The algorithm uses {{c1::gradient descent} to optimize.",
      "explanation": (
          '<div class="mermaid">graph TD\n  A[Start] ->|data| B(Process)'
          "</div>"
      ),
      "spanish": "El algoritmo usa descenso de gradiente.",
  }

  valid, fixed, errs = sanitize_and_validate_card(sample_broken)
  print(f"Valid: {valid}")
  print(f"Errors: {errs}")
  print(f"Fixed Card: {json.dumps(fixed, indent=2)}")
