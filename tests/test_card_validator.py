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

    def test_nested_card_validation_success_t17_conceptual(self):
        sample_card = {
            "id": "t17_test_01",
            "deck": "Social_and_Humanities::Philosophy::Stoicism::Ethics",
            "template": "T17_ConceptualModel",
            "metadata": {
                "difficulty": "intermediate",
                "pillar": "04_Social_and_Humanities",
                "tags": ["philosophy"]
            },
            "content": {
                "premise": "Dichotomy of Control",
                "explanation": "Understanding what is in our control and what is not.",
                "analogy": "An archer doing their best to shoot but accepting if the wind blows the arrow off-course.",
                "common_fallacies": "Assuming control of others' actions or being completely indifferent to results."
            }
        }
        is_valid, cleaned, errors = sanitize_and_validate_card(sample_card)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")

    def test_nested_card_validation_success_t18_system_architecture(self):
        sample_card = {
            "id": "t18_test_01",
            "deck": "Cloud_and_Infrastructure::Systems_Engineering::Linux::Kernel",
            "template": "T18_SystemArchitecture",
            "metadata": {
                "difficulty": "advanced",
                "pillar": "01_Cloud_and_Infrastructure",
                "tags": ["linux", "kernel"]
            },
            "content": {
                "design_problem": "Optimize socket buffers read capacity under high TCP traffic load.",
                "code_or_command": "sysctl -w net.ipv4.tcp_rmem='4096 87380 6291456'",
                "orchestration_context": "Configure system sysctl.conf on start or inside privileged daemonset init-container.",
                "expected_output": "net.ipv4.tcp_rmem = 4096 87380 6291456",
                "complexity_big_o": "O(1) memory overhead adjustment per socket connection buffer limit"
            }
        }
        is_valid, cleaned, errors = sanitize_and_validate_card(sample_card)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")

    def test_nested_card_validation_success_t19_phonetics(self):
        sample_card = {
            "id": "t19_test_01",
            "deck": "Languages::English::Phonetics::Flaps",
            "template": "T19_PhoneticDrill",
            "metadata": {
                "difficulty": "beginner",
                "pillar": "03_Languages",
                "tags": ["flapt"]
            },
            "content": {
                "target_phrase": "Water under the bridge.",
                "ipa_transcription": "/ˈwɔːtər ˈʌndər ðə brɪdʒ/",
                "audio_path": "audio/flaps/water_bridge.mp3",
                "phonological_rules": "Intervocalic T flap between stressed and unstressed vowels.",
                "register_context": "Casual spoken English."
            }
        }
        is_valid, cleaned, errors = sanitize_and_validate_card(sample_card)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")

    def test_nested_card_validation_success_t20_decision(self):
        sample_card = {
            "id": "t20_test_01",
            "deck": "Soft_Skills_and_Leadership::Leadership::Management::Crisis",
            "template": "T20_DecisionScenario",
            "metadata": {
                "difficulty": "advanced",
                "pillar": "05_Soft_Skills_and_Leadership",
                "tags": ["crisis"]
            },
            "content": {
                "scenario": "A major security exploit is active in production.",
                "options": [
                    "Isolate production database immediately, causing downtime.",
                    "Keep system running while debugging live to minimize impact."
                ],
                "consequences": "Downtime cuts revenue but preserves customer data safety.",
                "success_metric": "Customer data breach rate = 0%"
            }
        }
        is_valid, cleaned, errors = sanitize_and_validate_card(sample_card)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")

    def test_nested_card_validation_success_t21_interview_prep(self):
        sample_card = {
            "id": "t21_test_01",
            "deck": "Soft_Skills_and_Leadership::Leadership::Communication::Interview",
            "template": "T21_InterviewPrep",
            "metadata": {
                "difficulty": "advanced",
                "pillar": "05_Soft_Skills_and_Leadership",
                "tags": ["interview", "communication"]
            },
            "content": {
                "question": "How do Transformers leverage Attention mechanism?",
                "target_persona": "Software Engineer Lead",
                "rubric_checkpoints": [
                    "Explain Query, Key, Value vectors",
                    "Compare scaled dot-product attention formula",
                    "Mention O(N^2) complexity"
                ],
                "communication_cues": [
                    "Keep structure clean: Intro, Formula, Complexity",
                    "Avoid saying 'like'"
                ],
                "follow_up_hooks": [
                    "How does Linear Attention optimize this complexity?"
                ],
                "explanation": "Transformers calculate scaled dot-product attention using Query and Key...",
                "spanish": "Explicación en español..."
            }
        }
        is_valid, cleaned, errors = sanitize_and_validate_card(sample_card)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")

    def test_nested_card_validation_failure_t21_missing_fields(self):
        sample_card = {
            "id": "t21_test_02",
            "deck": "Soft_Skills_and_Leadership::Leadership::Communication::Interview",
            "template": "T21_InterviewPrep",
            "metadata": {
                "difficulty": "advanced",
                "pillar": "05_Soft_Skills_and_Leadership",
                "tags": ["interview"]
            },
            "content": {
                "question": "How do Transformers leverage Attention mechanism?",
                "target_persona": "Software Engineer Lead"
                # Missing rubric_checkpoints, cues, hooks, explanation, spanish
            }
        }
        is_valid, cleaned, errors = sanitize_and_validate_card(sample_card)
        self.assertFalse(is_valid)
        self.assertTrue(any("missing required fields" in err.lower() for err in errors))

if __name__ == "__main__":
    unittest.main()
