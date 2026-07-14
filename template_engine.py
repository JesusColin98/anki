#!/usr/bin/env python3
"""Multi-Template Engine for Anki Flashcards.

Implements 6 specialized Wozniak-aligned card templates:
- T1: Atomic Cloze Deletion
- T2: Dual-Coding Mermaid / Visual
- T3: Code Snippet & Algorithmic Pattern
- T4: Scenario & Soft Skills Dialogue
- T5: MathJax Formula & Physical Law
- T6: Active Recall Multiple Choice Quiz
"""

import json
from typing import Any, Dict, List

TEMPLATES = {
    "T1_Cloze": {
        "description": "Atomic Cloze Deletion for vocabulary and core facts",
        "required_fields": ["deck", "text", "explanation", "spanish"],
    },
    "T2_DualCoding": {
        "description": "Dual-Coding visual representation with Mermaid graph",
        "required_fields": [
            "deck",
            "concept",
            "mermaid_code",
            "explanation",
            "spanish",
        ],
    },
    "T3_CodeSnippet": {
        "description": "Code patterns, algorithms, and CLI commands",
        "required_fields": [
            "deck",
            "title",
            "code_block",
            "language",
            "explanation",
        ],
    },
    "T4_Scenario": {
        "description": "Real-world professional scenarios & negotiation",
        "required_fields": [
            "deck",
            "scenario",
            "target_phrase",
            "usage",
            "spanish",
        ],
    },
    "T5_MathJax": {
        "description": "LaTeX/MathJax formulas and physical laws",
        "required_fields": [
            "deck",
            "concept",
            "formula_latex",
            "variable_breakdown",
        ],
    },
    "T6_Quiz": {
        "description": "Active recall quiz with multiple choice options",
        "required_fields": [
            "deck",
            "question",
            "options",
            "correct_option",
            "rationale",
        ],
    },
    "T7_Pronunciation": {
        "description": "Pronunciation drills with connected speech rules",
        "required_fields": [
            "deck",
            "rule_name",
            "formal_phrase",
            "fast_pronunciation",
            "explanation",
            "spanish",
        ],
    },
}


def render_t1_cloze(data: Dict[str, Any]) -> Dict[str, Any]:
  return {
      "deck": data["deck"],
      "scenario": data.get("scenario", "Atomic Concept 🧠"),
      "text": data["text"],
      "explanation": data["explanation"],
      "usage": data.get("usage", f"Key Term: <code>{data['text']}</code>"),
      "spanish": data["spanish"],
      "tags": data.get("tags", ["wozniak_t1_cloze"]),
  }


def render_t2_dualcoding(data: Dict[str, Any]) -> Dict[str, Any]:
  mermaid_html = f"""<div class=\"mermaid\">\n{data['mermaid_code']}\n</div>"""
  return {
      "deck": data["deck"],
      "scenario": f"Dual-Coding Diagram 📊 ({data['concept']})",
      "text": (
          f"¿Cómo funciona la estructura de {{c1::{data['concept']}}} en el"
          " sistema?"
      ),
      "explanation": f"{data['explanation']}<br><br>{mermaid_html}",
      "usage": (
          f"Visual model for <code>{data['concept']}</code>.<br>Graph:"
          f" {mermaid_html}"
      ),
      "spanish": data["spanish"],
      "tags": data.get("tags", ["wozniak_t2_dualcoding"]),
  }


def render_t3_codesnippet(data: Dict[str, Any]) -> Dict[str, Any]:
  lang = data.get("language", "python")
  code_formatted = (
      f"<pre><code class=\"language-{lang}\">{data['code_block']}</code></pre>"
  )
  return {
      "deck": data["deck"],
      "scenario": f"Code Pattern 💻 ({data['title']})",
      "text": (
          f"Patrón de código en <b>{lang}</b> para"
          f" {{c1::{data['title']}}}:<br>{code_formatted}"
      ),
      "explanation": data["explanation"],
      "usage": (
          f"Snippet: {code_formatted}<br>Output expected:"
          f" <code>{data.get('expected_output', 'Success')}</code>"
      ),
      "spanish": f"Patrón de código: {data['title']}",
      "tags": data.get("tags", ["wozniak_t3_codesnippet", lang]),
  }


def render_t4_scenario(data: Dict[str, Any]) -> Dict[str, Any]:
  return {
      "deck": data["deck"],
      "scenario": data["scenario"],
      "text": (
          f"In this situation, you should say: \"{{c1::{data['target_phrase']}}}\""
      ),
      "explanation": data.get(
          "explanation", f"Professional phrase for: {data['scenario']}"
      ),
      "usage": data["usage"],
      "spanish": data["spanish"],
      "tags": data.get("tags", ["wozniak_t4_scenario"]),
  }


def render_t5_mathjax(data: Dict[str, Any]) -> Dict[str, Any]:
  formula = data["formula_latex"]
  return {
      "deck": data["deck"],
      "scenario": f"Math & Physics 📐 ({data['concept']})",
      "text": f"Ecuación para {{c1::{data['concept']}}}: \\[{formula}\\]",
      "explanation": (
          f"Desglose de variables: <ul>{data['variable_breakdown']}</ul>"
      ),
      "usage": f"Formula: \\[{formula}\\]",
      "spanish": f"Fórmula de {data['concept']}",
      "tags": data.get("tags", ["wozniak_t5_mathjax"]),
  }


def render_t6_quiz(data: Dict[str, Any]) -> Dict[str, Any]:
  options_html = "".join([f"<li>{opt}</li>" for opt in data["options"]])
  return {
      "deck": data["deck"],
      "scenario": "Active Recall Quiz 🎯",
      "text": (
          f"<b>Pregunta:</b> {data['question']}<br>Opciones:<ul>{options_html}</ul><br>Respuesta"
          f" correcta: {{c1::{data['correct_option']}}}"
      ),
      "explanation": f"Justificación: {data['rationale']}",
      "usage": f"Quiz assertion: {data['correct_option']}",
      "spanish": f"Quiz: {data['question']}",
      "tags": data.get("tags", ["wozniak_t6_quiz"]),
  }


def render_t7_pronunciation(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "deck": data["deck"],
        "scenario": f"Pronunciation Drill: {data['rule_name']} 🗣️",
        "text": f"Practice saying this phrase fast: \"<b>{data['formal_phrase']}</b>\"<br>Connected speech pronunciation: {{{{c1::{data['fast_pronunciation']}}}}}",
        "explanation": f"Applied Rule: <b>{data['rule_name']}</b><br>{data['explanation']}",
        "usage": f"Formal: <code>{data['formal_phrase']}</code> &rarr; Connected: <code>{data['fast_pronunciation']}</code>",
        "spanish": f"Spanish: {data['spanish']}",
        "tags": data.get("tags", ["pronunciation_drill", data['rule_name'].lower().replace(" ", "_")]),
    }


from card_validator import sanitize_and_validate_card

def build_card(template_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Constructs and deterministically validates an Anki card matching template_type."""
    if template_type not in TEMPLATES:
        raise ValueError(f"Unknown template: {template_type}. Valid options: {list(TEMPLATES.keys())}")
        
    reqs = TEMPLATES[template_type]["required_fields"]
    missing = [f for f in reqs if f not in data]
    if missing:
        raise ValueError(f"Missing required fields for {template_type}: {missing}")
        
    raw_card = None
    if template_type == "T1_Cloze":
        raw_card = render_t1_cloze(data)
    elif template_type == "T2_DualCoding":
        raw_card = render_t2_dualcoding(data)
    elif template_type == "T3_CodeSnippet":
        raw_card = render_t3_codesnippet(data)
    elif template_type == "T4_Scenario":
        raw_card = render_t4_scenario(data)
    elif template_type == "T5_MathJax":
        raw_card = render_t5_mathjax(data)
    elif template_type == "T6_Quiz":
        raw_card = render_t6_quiz(data)
    elif template_type == "T7_Pronunciation":
        raw_card = render_t7_pronunciation(data)
        
    # Run deterministic validation & auto-repair pipeline
    is_valid, cleaned_card, validation_errors = sanitize_and_validate_card(raw_card)
    if validation_errors:
        print(f"[!] Deterministic Validator Warning for {template_type}: {validation_errors}")
        
    return cleaned_card


if __name__ == "__main__":
  sample_t3 = {
      "deck": "AI_Learning_Path::04_Agentic_Systems",
      "title": "ADK State Sharing",
      "code_block": "state.set('key', 'value')",
      "language": "python",
      "explanation": "State sharing allows subagents to exchange data.",
  }
  card = build_card("T3_CodeSnippet", sample_t3)
  print(json.dumps(card, indent=2, ensure_ascii=False))
