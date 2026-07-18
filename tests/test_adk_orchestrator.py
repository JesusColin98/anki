#!/usr/bin/env python3
"""Unit tests for the ADK Orchestrator cognitive routing and loop controls."""

import unittest
from unittest.mock import patch
import sys
from pathlib import Path

# Ensure root is in sys.path
BASE_DIR = Path(__file__).parent.parent.resolve()
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from adk_orchestrator import process_chunk_with_guardrails


class TestAdkOrchestrator(unittest.TestCase):

    @patch("adk_orchestrator.route_chunk_complexity")
    @patch("adk_orchestrator.generate_anki_cards_gemini")
    def test_routing_simple(self, mock_generate, mock_route):
        # 1. Mock simple classification routing
        mock_route.return_value = "SIMPLE"
        
        # 2. Mock simple card generation output
        mock_generate.return_value = [
            {
                "template": "T1_Cloze",
                "scenario": "Concept",
                "text": "Active recall is a {{c1::learning}} technique.",
                "explanation": "Active recall is the principle of retrieving facts from memory.",
                "spanish": "El recuerdo activo es una técnica de aprendizaje.",
                "usage": "Practice: recall key facts."
            }
        ]

        deck_name = "06_Business_and_Productivity::Learning_and_Memory::Methodology::Recall"
        cards = process_chunk_with_guardrails(
            "Active recall is a learning technique.", deck_name
        )

        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["template"], "T1_Cloze")
        self.assertEqual(cards[0]["metadata"]["validation_status"], "valid")
        mock_route.assert_called_once()
        mock_generate.assert_called_once_with(
            "Active recall is a learning technique.", deck_name, complexity="SIMPLE"
        )

    @patch("adk_orchestrator.route_chunk_complexity")
    @patch("adk_orchestrator.generate_anki_cards_gemini")
    @patch("adk_orchestrator.correct_card_with_feedback")
    def test_self_repair_loop_success(self, mock_correct, mock_generate, mock_route):
        mock_route.return_value = "COMPLEX"
        
        # Initially generate a malformed card (missing required fields for T21)
        mock_generate.return_value = [
            {
                "template": "T21_InterviewPrep",
                "content": {
                    "question": "How does Attention work?",
                    "target_persona": "Software Lead"
                    # missing rubric_checkpoints, etc.
                }
            }
        ]

        # On self-correction, return a fully valid card
        mock_correct.return_value = {
            "template": "T21_InterviewPrep",
            "metadata": {
                "difficulty": "advanced",
                "tags": ["transformers"]
            },
            "content": {
                "question": "How does Attention work?",
                "target_persona": "Software Lead",
                "rubric_checkpoints": ["Mention Q, K, V"],
                "communication_cues": ["Stay calm"],
                "follow_up_hooks": ["Explain scale factor"],
                "explanation": "Attention matches Queries and Keys to weight Values...",
                "spanish": "El mecanismo de atención..."
            }
        }

        deck_name = "05_Soft_Skills_and_Leadership::Leadership::Communication::Interview"
        cards = process_chunk_with_guardrails("Attention chunk content.", deck_name)

        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["template"], "T21_InterviewPrep")
        self.assertEqual(cards[0]["metadata"]["validation_status"], "valid")
        mock_correct.assert_called_once()

    @patch("adk_orchestrator.route_chunk_complexity")
    @patch("adk_orchestrator.generate_anki_cards_gemini")
    @patch("adk_orchestrator.correct_card_with_feedback")
    def test_graceful_degradation_fallback(self, mock_correct, mock_generate, mock_route):
        mock_route.return_value = "COMPLEX"
        
        # Card that keeps failing validation
        broken_card = {
            "template": "T21_InterviewPrep",
            "content": {
                "question": "Uncorrectable question",
                "target_persona": "Software Lead"
            }
        }
        mock_generate.return_value = [broken_card]
        mock_correct.return_value = broken_card  # stays broken

        deck_name = "05_Soft_Skills_and_Leadership::Leadership::Communication::Interview"
        cards = process_chunk_with_guardrails("Broken chunk content.", deck_name)

        self.assertEqual(len(cards), 1)
        # Should degrade to low_confidence and import fallback
        self.assertEqual(cards[0]["metadata"]["validation_status"], "low_confidence")
        self.assertIn("needs_review", cards[0]["metadata"]["tags"])
        self.assertEqual(mock_correct.call_count, 3) # Max retries


if __name__ == "__main__":
    unittest.main()
