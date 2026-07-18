import pytest
import json
from unittest.mock import patch
from agentic_generator import run_agentic_loop

# Mock responses
VALID_CARDS_RESPONSE = {
    "cards": [
        {
            "scenario": "Fast English: Flap T ⚡ — Tier 1",
            "full_transcript": "water",
            "connected_form": "wa-der",
            "ipa_transcription": "/ˈwɑː.ɾər/",
            "gap_text": "wa-der is {{c1::wa-der}}",
            "rules_applied": ["Flap T"],
            "audio_search_forvo": "water",
            "audio_search_youglish": "water",
            "phonetic_breakdown": "The t becomes a flap.",
            "spanish": "agua",
            "language": "en",
            "tier": 1
        }
    ]
}

INVALID_CARDS_RESPONSE = {
    "cards": [
        {
            "scenario": "Missing stuff",
            "full_transcript": "water",
            # missing gap_text, connected_form, etc to trigger deterministic fail
        }
    ]
}

ACCEPT_EVAL_RESPONSE = {
    "accepted": True,
    "feedback": "Perfect!"
}

REJECT_EVAL_RESPONSE = {
    "accepted": False,
    "feedback": "No, fix the cloze."
}


@patch("agentic_generator.chat_completion")
def test_agentic_loop_success_first_try(mock_chat):
    """Test the loop when everything works on the first try with Ollama."""
    # First call: generation, Second call: evaluation
    mock_chat.side_effect = [
        json.dumps(VALID_CARDS_RESPONSE),
        json.dumps(ACCEPT_EVAL_RESPONSE)
    ]
    
    success, cards, attempts, elapsed = run_agentic_loop(rule_num=2, count=1, provider="ollama")
    
    assert success is True
    assert attempts == 1
    assert len(cards) == 1
    assert mock_chat.call_count == 2


@patch("agentic_generator.chat_completion")
def test_agentic_loop_retry_on_eval_reject(mock_chat):
    """Test that the loop retries if the evaluator rejects the cards."""
    mock_chat.side_effect = [
        json.dumps(VALID_CARDS_RESPONSE),      # Gen 1
        json.dumps(REJECT_EVAL_RESPONSE),      # Eval 1 (Reject)
        json.dumps(VALID_CARDS_RESPONSE),      # Gen 2
        json.dumps(ACCEPT_EVAL_RESPONSE)       # Eval 2 (Accept)
    ]
    
    success, cards, attempts, elapsed = run_agentic_loop(rule_num=2, count=1, provider="ollama")
    
    assert success is True
    assert attempts == 2
    assert len(cards) == 1
    assert mock_chat.call_count == 4


@patch("agentic_generator.chat_completion")
def test_agentic_loop_retry_on_deterministic_fail(mock_chat):
    """Test that the loop retries if deterministic validation fails."""
    mock_chat.side_effect = [
        json.dumps(INVALID_CARDS_RESPONSE),    # Gen 1 (Invalid schema)
        # Note: Eval is NOT called here because it fails deterministically
        json.dumps(VALID_CARDS_RESPONSE),      # Gen 2 (Valid)
        json.dumps(ACCEPT_EVAL_RESPONSE)       # Eval 1 (Accept)
    ]
    
    success, cards, attempts, elapsed = run_agentic_loop(rule_num=2, count=1, provider="ollama")
    
    assert success is True
    assert attempts == 2
    assert len(cards) == 1
    assert mock_chat.call_count == 3


@patch("agentic_generator.chat_completion")
def test_agentic_loop_exhaust_retries(mock_chat):
    """Test that the loop returns False after max retries are exhausted."""
    # Always reject
    mock_chat.side_effect = [
        json.dumps(VALID_CARDS_RESPONSE), json.dumps(REJECT_EVAL_RESPONSE),
        json.dumps(VALID_CARDS_RESPONSE), json.dumps(REJECT_EVAL_RESPONSE),
        json.dumps(VALID_CARDS_RESPONSE), json.dumps(REJECT_EVAL_RESPONSE),
    ]
    
    success, cards, attempts, elapsed = run_agentic_loop(rule_num=2, count=1, provider="ollama", max_retries=3)
    
    assert success is False
    assert attempts == 3
    assert len(cards) == 0
    assert mock_chat.call_count == 6
