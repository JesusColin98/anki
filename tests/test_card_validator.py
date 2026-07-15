#!/usr/bin/env python3
"""Unit tests for Card Validator & Pydantic V2 Schema Validation."""

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

    def test_mathjax_unbalanced(self):
        unbalanced = "Equation: \\[E = mc^2"
        is_valid, errors = validate_mathjax_delimiters(unbalanced)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)

    def test_nested_card_validation_success_t1(self):
        sample_card = {
            "id": "c1a2b3d4",
            "deck": "Cybersecurity::Red_Teaming::Exploitation",
            "template": "T1_Cloze",
            "metadata": {
                "difficulty": "intermediate",
                "pillar": "01_Cloud_and_Infrastructure",
                "tags": ["buffer_overflow"]
            },
            "content": {
                "scenario": "Linux Exploit: Stack Smash ⚡",
                "text": "The stack frame pointer is overwritten using {{c1::buffer overflow}}.",
                "explanation": "Overwriting return address redirects code execution flow.",
                "spanish": "Desbordamiento de búfer.",
                "usage": "Trigger payload: <code>cat exploit.bin | nc target 80</code>"
            }
        }
        is_valid, cleaned, errors = sanitize_and_validate_card(sample_card)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")
        self.assertEqual(cleaned["template"], "T1_Cloze")
        self.assertEqual(cleaned["metadata"]["difficulty"], "intermediate")

    def test_nested_card_validation_failure_t1_missing_field(self):
        # Missing 'spanish' under content
        sample_card = {
            "id": "c1a2b3d4",
            "deck": "Cybersecurity::Red_Teaming::Exploitation",
            "template": "T1_Cloze",
            "metadata": {
                "difficulty": "intermediate",
                "pillar": "01_Cloud_and_Infrastructure",
                "tags": ["buffer_overflow"]
            },
            "content": {
                "scenario": "Linux Exploit: Stack Smash ⚡",
                "text": "The stack frame pointer is overwritten using {{c1::buffer overflow}}.",
                "explanation": "Overwriting return address redirects code execution flow."
            }
        }
        is_valid, cleaned, errors = sanitize_and_validate_card(sample_card)
        self.assertFalse(is_valid)
        self.assertTrue(any("missing required fields" in err.lower() for err in errors))

    def test_nested_card_validation_success_t13_palace(self):
        sample_card = {
            "id": "p123abcd",
            "deck": "Productivity::Memory_Techniques::Study",
            "template": "T13_MnemonicPalace",
            "metadata": {
                "difficulty": "advanced",
                "pillar": "06_Business_and_Productivity",
                "tags": ["memory_craft"]
            },
            "content": {
                "concept": "Method of Loci",
                "explanation": "Anchoring details to physical rooms in a journey.",
                "spanish": "Método de Loci"
            },
            "mnemonics": {
                "palace_name": "My Bedroom",
                "locus_stop": "01_Desk_Lamp",
                "mnemonic_scene": "A massive floating brain lighting up the desk lamp."
            }
        }
        is_valid, cleaned, errors = sanitize_and_validate_card(sample_card)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")

    def test_nested_card_validation_failure_t13_missing_mnemonics(self):
        # Missing palace_name/locus_stop/mnemonic_scene values in mnemonics
        sample_card = {
            "id": "p123abcd",
            "deck": "Productivity::Memory_Techniques::Study",
            "template": "T13_MnemonicPalace",
            "metadata": {
                "difficulty": "advanced",
                "pillar": "06_Business_and_Productivity",
                "tags": ["memory_craft"]
            },
            "content": {
                "concept": "Method of Loci",
                "explanation": "Anchoring details to physical rooms in a journey.",
                "spanish": "Método de Loci"
            },
            "mnemonics": {
                "palace_name": "", # empty
                "locus_stop": "01_Desk_Lamp",
                "mnemonic_scene": "" # empty
            }
        }
        is_valid, cleaned, errors = sanitize_and_validate_card(sample_card)
        self.assertFalse(is_valid)
        self.assertTrue(any("requires palace_name, locus_stop, and mnemonic_scene" in err for err in errors))

if __name__ == "__main__":
    unittest.main()
