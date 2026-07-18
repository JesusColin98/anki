#!/usr/bin/env python3
"""Gemini LLM Provider for generating high-quality Anki cards.

Communicates with Gemini Developer API to produce structured Wozniak-compliant cards.
"""

import json
import os
import requests
from typing import List, Dict, Any
from pathlib import Path

def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("GEMINI_API_KEY="):
                    return line.strip().split("=", 1)[1].strip().strip("'\"")
    return ""

GEMINI_API_KEY = get_api_key()

def get_gemini_url(model: str = "gemini-2.5-pro") -> str:
    return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"

def route_chunk_complexity(chunk_text: str) -> str:
    """Calls Gemini 2.5 Flash to classify chunk complexity.
    
    Returns 'SIMPLE' or 'COMPLEX'.
    """
    url = get_gemini_url("gemini-2.5-flash")
    system_instruction = (
        "You are a cognitive triage router. Analyze the text chunk and classify it. "
        "Return exactly one word: 'SIMPLE' or 'COMPLEX'.\n"
        "- SIMPLE: Basic vocabulary, factual listings, simple dictionary terms, or uncomplicated definitions.\n"
        "- COMPLEX: Multi-step system architectures, complex logical systems, soft skills, conversational dialogs, "
        "phonetics rules, or decision-making scenarios."
    )
    
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": f"{system_instruction}\n\nContent:\n{chunk_text}"}]
        }],
        "generationConfig": {
            "temperature": 0.0,
            "maxOutputTokens": 10
        }
    }
    
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        result = resp.json()
        raw_text = result["candidates"][0]["content"]["parts"][0]["text"].strip().upper()
        if "COMPLEX" in raw_text:
            return "COMPLEX"
        return "SIMPLE"
    except Exception as e:
        print(f"[-] Triage routing error: {e}. Defaulting to COMPLEX.")
        return "COMPLEX"

def generate_anki_cards_gemini(prompt_text: str, deck_name: str, complexity: str = "COMPLEX") -> List[Dict[str, Any]]:
    """Calls Gemini API to generate structured, high-quality Anki cards.
    
    If complexity is SIMPLE, uses gemini-2.5-flash and only generates T1_Cloze cards.
    If complexity is COMPLEX, uses gemini-2.5-pro and can generate all card templates (T1-T21).
    """
    model = "gemini-2.5-flash" if complexity == "SIMPLE" else "gemini-2.5-pro"
    url = get_gemini_url(model)
    
    if complexity == "SIMPLE":
        system_instruction = (
            "You are an expert Anki card generator. Generate a list of simple, highly atomic cards "
            "following Wozniak's 20 Rules of Formulating Knowledge. Each card must target exactly one fact "
            "using a cloze deletion. You must respond with a JSON object containing "
            "a 'cards' key with an array of objects. Each card object must have: 'deck', 'template', 'scenario', 'text', 'explanation', 'usage', 'spanish', 'tags'."
        )
        user_prompt = f"""
        Analyze the following text and extract basic facts. Create between 2 to 4 high-quality T1_Cloze cards.
        Rules for fields:
        1. 'deck': Must be exactly "{deck_name}".
        2. 'template': Must be "T1_Cloze".
        3. 'scenario': Short category + emoji (e.g. "Concept 🧠: Definition").
        4. 'text': The card front with exactly one balanced cloze deletion (e.g., "The {{c1::term}} is...").
        5. 'explanation': Clear explanation of why (2+ sentences).
        6. 'usage': Styled HTML list containing examples.
        7. 'spanish': Natural Spanish translation.
        8. 'tags': Relevant lowercase tags.

        Content to analyze:
        {prompt_text}

        Format output strictly as JSON object with key 'cards':
        {{
          "cards": [
            {{
              "deck": "{deck_name}",
              "template": "T1_Cloze",
              "scenario": "...",
              "text": "...",
              "explanation": "...",
              "usage": "...",
              "spanish": "...",
              "tags": ["tag1"]
            }}
          ]
        }}
        """
    else:
        system_instruction = (
            "You are an expert Anki card generator. Generate a list of highly structured cards "
            "following Wozniak's 20 Rules of Formulating Knowledge. You have access to these templates:\n"
            "- T1_Cloze: text (with exactly one {{c1::...}}), explanation, spanish\n"
            "- T2_DualCoding: concept, mermaid_code (arrows must be -->), explanation, spanish\n"
            "- T3_CodeSnippet: title, code_block, language, explanation\n"
            "- T4_Scenario: scenario, target_phrase, usage, spanish\n"
            "- T5_MathJax: concept, formula_latex, variable_breakdown\n"
            "- T6_Quiz: question, options, correct_option, rationale\n"
            "- T17_ConceptualModel: premise, explanation, analogy, common_fallacies\n"
            "- T18_SystemArchitecture: design_problem, code_or_command, orchestration_context, expected_output, complexity_big_o\n"
            "- T19_PhoneticDrill: target_phrase, ipa_transcription, audio_path, phonological_rules, register_context\n"
            "- T20_DecisionScenario: scenario, options, consequences, success_metric\n"
            "- T21_InterviewPrep: question, target_persona, rubric_checkpoints, communication_cues, follow_up_hooks, explanation, spanish\n"
            "Choose the best templates to capture the content. Format the JSON strictly using the nested schema structure."
        )
        user_prompt = f"""
        Analyze the following complex content and generate between 2 to 5 structured cards.
        Rules for fields:
        1. 'deck': Must be exactly "{deck_name}".
        2. 'template': Must specify the exact template ID (e.g. 'T21_InterviewPrep', 'T18_SystemArchitecture', etc.).
        3. 'metadata': {{ "difficulty": "intermediate"|"advanced", "tags": [...] }}
        4. 'content': Nested dictionary containing the specific template fields (e.g., for T21: question, target_persona, rubric_checkpoints, etc.).
        
        Content to analyze:
        {prompt_text}

        Format output strictly as a JSON object with key 'cards':
        {{
          "cards": [
             {{
               "deck": "{deck_name}",
               "template": "T21_InterviewPrep",
               "metadata": {{ "difficulty": "advanced", "tags": ["tag1"] }},
               "content": {{
                  "question": "...",
                  "target_persona": "...",
                  "rubric_checkpoints": ["...", "..."],
                  "communication_cues": ["...", "..."],
                  "follow_up_hooks": ["...", "..."],
                  "explanation": "...",
                  "spanish": "..."
               }}
             }}
          ]
        }}
        """

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"{system_instruction}\n\n{user_prompt}"}]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }

    headers = {"Content-Type": "application/json"}

    print(f"[+] Invoking Gemini API ({model}) for deck '{deck_name}'...")
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        
        content = result["candidates"][0]["content"]["parts"][0]["text"]
        data = json.loads(content)
        
        cards = data.get("cards", data) if isinstance(data, dict) else data
        if not isinstance(cards, list):
            if isinstance(data, dict) and "deck" in data:
                cards = [data]
            else:
                cards = []
        
        for card in cards:
            if isinstance(card, dict):
                card["deck"] = deck_name

        return cards
    except Exception as e:
        print(f"[-] Gemini API card generation error: {e}")
        return []

def correct_card_with_feedback(card_data: dict, errors: List[str]) -> dict:
    """Invokes Gemini 2.5 Pro to fix a card that failed validation.
    
    Provides the original card data and specific validation errors as context.
    """
    url = get_gemini_url("gemini-2.5-pro")
    system_instruction = (
        "You are an expert card corrector. You will be given a JSON object representing an Anki card "
        "and a list of syntax or schema validation errors. Correct the card so it passes all validations. "
        "Keep the core conceptual value intact. Return only the corrected card as a JSON object."
    )
    
    user_prompt = f"""
    Malformed Card:
    {json.dumps(card_data, indent=2, ensure_ascii=False)}
    
    Validation Errors:
    {json.dumps(errors, indent=2, ensure_ascii=False)}
    
    Please fix the card and output only the corrected JSON.
    """
    
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": f"{system_instruction}\n\n{user_prompt}"}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1
        }
    }
    
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=25)
        resp.raise_for_status()
        result = resp.json()
        content = result["candidates"][0]["content"]["parts"][0]["text"]
        fixed = json.loads(content)
        return fixed
    except Exception as e:
        print(f"[-] Failed to self-correct card: {e}")
        return card_data

if __name__ == "__main__":
    sample_text = (
        "Principal Component Analysis (PCA) is an unsupervised learning technique used for "
        "dimensionality reduction. It works by projecting the data onto orthogonal axes that maximize "
        "variance, known as principal components. The first principal component accounts for the largest "
        "possible variance in the dataset."
    )
    # Test simple/complex routing
    comp = route_chunk_complexity(sample_text)
    print(f"Routed complexity: {comp}")
    cards = generate_anki_cards_gemini(sample_text, "02_AI_and_Data_Science::Classical_ML::Overview::PCA", complexity=comp)
    print(json.dumps(cards, indent=2, ensure_ascii=False))
