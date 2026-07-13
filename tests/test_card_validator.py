#!/usr/bin/env python3
"""Unit tests for Card Validator & Deterministic Auto-Repair Engine."""

import sys
import unittest
from pathlib import Path

# Ensure repo root is on sys.path
BASE_DIR = Path(__file__).parent.parent.resolve()
if str(BASE_DIR) not in sys.path:
  sys.path.insert(0, str(BASE_DIR))

from card_validator import (
    sanitize_and_validate_card,
    sanitize_mermaid_code,
    validate_cloze_syntax,
    validate_mathjax_delimiters,
)


class TestCardValidator(unittest.TestCase):

  def test_cloze_syntax_repair(self):
    unclosed_cloze = "This is {{c1::unclosed tag} in text."
    is_valid, repaired, errors = validate_cloze_syntax(unclosed_cloze)
    self.assertTrue(is_valid)
    self.assertIn("{{c1::unclosed tag}}", repaired)

  def test_mermaid_arrow_and_quote_repair(self):
    broken_mermaid = "graph TD\n  NodeA[Start Process] ->|payload| NodeB(End)"
    repaired = sanitize_mermaid_code(broken_mermaid)
    self.assertIn("-->|payload|", repaired)
    self.assertIn('NodeA["Start Process"]', repaired)

  def test_mathjax_balancing(self):
    balanced = "Equation: \\[E = mc^2\\] and inline \\(a^2 + b^2 = c^2\\)"
    is_valid, errors = validate_mathjax_delimiters(balanced)
    self.assertTrue(is_valid)
    self.assertEqual(len(errors), 0)

  def test_full_card_sanitization(self):
    sample_card = {
        "deck": "Test::Deck",
        "text": "Concept {{c1::active recall}",
        "explanation": (
            '<div class="mermaid">graph TD\n  A[Start] ->|data| B(End)</div>'
        ),
        "spanish": "Prueba",
    }
    is_valid, cleaned, errors = sanitize_and_validate_card(sample_card)
    self.assertTrue(is_valid)
    self.assertIn("{{c1::active recall}}", cleaned["text"])
    self.assertIn("-->|data|", cleaned["explanation"])


if __name__ == "__main__":
  unittest.main()
