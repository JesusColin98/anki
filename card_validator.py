#!/usr/bin/env python3
"""Deterministic Card & Syntax Validator for Anki Flashcards (Pydantic V2 Upgrade).

Enforces strict type validation and structural compliance across 16 templates:
1. Type safety and structure validation via Pydantic V2.
2. Template-specific required content field validation.
3. Mandatory mnemonic schema checks for T13 and T14.
4. Auto-repair and syntax parsing for Clozes, Mermaid graphs, and MathJax.
"""

import json
import re
from typing import List, Tuple, Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator, ValidationError

# ===========================================================================
# PYDANTIC SCHEMAS FOR NESTED ANKI CARDS
# ===========================================================================

class CardMetadata(BaseModel):
    difficulty: str = Field(default="intermediate")
    pillar: str
    tags: List[str] = Field(default_factory=list)

class CardMnemonics(BaseModel):
    palace_name: str = ""
    locus_stop: str = ""
    mnemonic_scene: str = ""
    peg_word: str = ""
    phonetic_code: str = ""

class CardInteractivity(BaseModel):
    analogy: str = ""
    interactive_mermaid: str = ""
    match_game_data: Optional[Dict[str, Any]] = None

class CardNestedSchema(BaseModel):
    id: str
    deck: str
    template: str
    metadata: CardMetadata
    content: Dict[str, Any]
    mnemonics: CardMnemonics = Field(default_factory=CardMnemonics)
    interactivity: CardInteractivity = Field(default_factory=CardInteractivity)

    @model_validator(mode='after')
    def validate_content_fields(self):
        # Maps template to required fields in card['content']
        req_content_fields = {
            "T1_Cloze": ["text", "explanation", "spanish"],
            "T2_DualCoding": ["concept", "mermaid_code", "explanation", "spanish"],
            "T3_CodeSnippet": ["title", "code_block", "language", "explanation"],
            "T4_Scenario": ["scenario", "target_phrase", "usage", "spanish"],
            "T5_MathJax": ["concept", "formula_latex", "variable_breakdown"],
            "T6_Quiz": ["question", "options", "correct_option", "rationale"],
            "T7_Pronunciation": ["rule_name", "formal_phrase", "fast_pronunciation", "explanation", "spanish"],
            "T8_MinimalPair": ["phoneme_a", "phoneme_b", "ipa_a", "ipa_b", "word_pairs", "muscle_tip", "language"],
            "T9_ListeningChunk": ["full_transcript", "connected_form", "gap_text", "rules_applied", "language"],
            "T10_ReadingPatternDrill": ["language", "script_note", "grapheme_pattern", "word_examples", "phoneme_target"],
            "T11_ExecutivePitch": ["speaker", "source_context", "transcript_excerpt", "pitch_analysis", "pause_map", "shadowing_script", "leadership_technique"],
            "T12_SpeakingPractice": ["prompt", "explanation", "usage", "spanish", "model_audio_url", "practice_url"],
            "T13_MnemonicPalace": ["concept", "explanation", "spanish"],
            "T14_PegNumber": ["concept", "number", "phonetic_code", "peg_word", "visual_scene"],
            "T15A_FeynmanAnalogy": ["concept", "layperson_explanation", "metaphor_analogy", "explanation"],
            "T15B_FeynmanScenario": ["concept", "generation_challenge", "explanation"],
            "T16_NameFace": ["person_name", "distinguishing_feature", "substitute_word_or_image", "association_scene", "contribution"]
        }
        
        tpl = self.template
        if tpl not in req_content_fields:
            raise ValueError(f"Unknown template: '{tpl}'")
            
        req_fields = req_content_fields[tpl]
        missing = [f for f in req_fields if f not in self.content or not str(self.content[f]).strip()]
        if missing:
            raise ValueError(f"Template '{tpl}' content is missing required fields: {missing}")
            
        # T13 Mnemonic Palace validation
        if tpl == "T13_MnemonicPalace":
            m = self.mnemonics
            if not m.palace_name.strip() or not m.locus_stop.strip() or not m.mnemonic_scene.strip():
                raise ValueError("T13_MnemonicPalace requires palace_name, locus_stop, and mnemonic_scene in mnemonics.")
                
        # T14 Peg Number validation
        if tpl == "T14_PegNumber":
            m = self.mnemonics
            if not m.peg_word.strip() or not m.phonetic_code.strip():
                raise ValueError("T14_PegNumber requires peg_word and phonetic_code in mnemonics.")
                
        return self

# ===========================================================================
# SANITIZERS & DETERMINISTIC PARSERS
# ===========================================================================

def sanitize_mermaid_code(mermaid_code: str) -> str:
    """Sanitizes and repairs common Mermaid syntax errors produced by LLMs."""
    code = mermaid_code.strip()

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

    def quote_label(match):
        node_id = match.group(1)
        bracket_type = match.group(2)
        label = match.group(3).strip()
        close_bracket = match.group(4)

        if (
            label.startswith('"')
            and label.endswith('"')
            or label.startswith("'")
            and label.endswith("'")
        ):
            return match.group(0)

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

    # Check for cloze pattern if there is any indication of a cloze tag
    if "{{" in repaired_text or "}}" in repaired_text:
        cloze_pattern = r"\{\{c\d+::.*?\}\}"
        matches = re.findall(cloze_pattern, repaired_text)
        if not matches:
            errors.append("Malformed or unclosed Cloze deletion tag {{c1::...}} found.")

    return len(errors) == 0, repaired_text, errors


def validate_mathjax_delimiters(text: str) -> Tuple[bool, List[str]]:
    """Checks that MathJax delimiters \\[...\\] and \\(...\\) are balanced."""
    errors = []
    block_open = text.count("\\[")
    block_close = text.count("\\]")
    inline_open = text.count("\\(")
    inline_close = text.count("\\)")

    if block_open != block_close:
        errors.append(f"Unbalanced block MathJax delimiters: \\[ ({block_open}) vs \\] ({block_close})")
    if inline_open != inline_close:
        errors.append(f"Unbalanced inline MathJax delimiters: \\( ({inline_open}) vs \\) ({inline_close})")

    return len(errors) == 0, errors


def validate_cognitive_rules(card: dict, strict: bool = False) -> List[str]:
    """Applies cognitive usability and spaced repetition rules.
    
    If strict=True, uses strict limits (e.g. 80 chars for cloze answer).
    Otherwise, uses relaxed limits (e.g. 150 chars for cloze answer).
    """
    warnings = []
    
    # Extract fields
    content = card.get("content", {})
    if not isinstance(content, dict):
        content = card # Fallback if flat
        
    text = content.get("text", content.get("prompt", ""))
    explanation = content.get("explanation", "")
    
    # 1. Cloze count limit: Max 2 cloze deletions of any index per card
    clozes = re.findall(r"\{\{c\d+::.*?\}\}", text)
    if len(clozes) > 2:
        warnings.append(f"Cognitive: Card has {len(clozes)} cloze deletions. Max 2 allowed per card to maintain atomicity.")
        
    # 2. Cloze content length check
    cloze_limit = 80 if strict else 150
    for cloze in clozes:
        content_match = re.search(r"\{\{c\d+::(.*?)\}\}", cloze)
        if content_match:
            cloze_text = content_match.group(1)
            # Remove HTML tags inside cloze text
            cloze_text_clean = re.sub(r"<[^>]+>", "", cloze_text).strip()
            if len(cloze_text_clean) > cloze_limit:
                warnings.append(
                    f"Cognitive: Cloze answer '{cloze_text_clean[:20]}...' is {len(cloze_text_clean)} characters long. "
                    f"Max {cloze_limit} allowed in {'strict' if strict else 'relaxed'} mode to avoid walls of text."
                )
                
    # 3. Prompt/Text length check to avoid ambiguity
    if text:
        # Clean text from clozes and HTML
        clean_text = re.sub(r"\{\{c\d+::(.*?)\}\}", r"\1", text)
        clean_text = re.sub(r"<[^>]+>", "", clean_text).strip()
        if len(clean_text) < 15:
            warnings.append(f"Cognitive: Prompt text is too short ({len(clean_text)} chars). Should be >= 15 chars to provide sufficient context.")
            
    # 4. Wall of Text check: Max 600 characters in the explanation if it doesn't contain tabs
    if explanation and len(explanation) > 600:
        if "tabs-container" not in explanation and "tab-btn" not in explanation:
            warnings.append(f"Cognitive: Explanation is too long ({len(explanation)} chars) and does not use tabs. Use tabs or split the concept.")
            
    return warnings


def sanitize_and_validate_card(card: dict) -> Tuple[bool, dict, List[str]]:
    """Deterministic validator pipeline for generated nested Anki cards."""
    errors = []
    
    # 1. Structural check: Must be a dict
    if not isinstance(card, dict):
        return False, card, ["Card must be a valid JSON dictionary."]

    # 2. Repair Clozes if present in content fields
    cleaned_card = card.copy()
    if "content" in cleaned_card and isinstance(cleaned_card["content"], dict):
        content = cleaned_card["content"]
        for field in ["text", "gap_text", "prompt"]:
            if field in content and isinstance(content[field], str):
                _, repaired_val, cloze_errs = validate_cloze_syntax(content[field])
                content[field] = repaired_val
                errors.extend(cloze_errs)
                
        # Repair Mermaid diagrams in content
        if "mermaid_code" in content and isinstance(content["mermaid_code"], str):
            content["mermaid_code"] = sanitize_mermaid_code(content["mermaid_code"])
            
        if "explanation" in content and isinstance(content["explanation"], str) and "class=\"mermaid\"" in content["explanation"]:
            def repair_mermaid_div(match):
                m_code = match.group(1)
                sanitized = sanitize_mermaid_code(m_code)
                return f'<div class="mermaid">\n{sanitized}\n</div>'

            content["explanation"] = re.sub(
                r'<div class="mermaid">\s*(.*?)\s*</div>',
                repair_mermaid_div,
                content["explanation"],
                flags=re.DOTALL,
            )

    # 3. Validate MathJax across all fields
    full_str = json.dumps(cleaned_card)
    _, math_errors = validate_mathjax_delimiters(full_str)
    errors.extend(math_errors)

    # 4. Strict structural validation using Pydantic V2
    try:
        validated_schema = CardNestedSchema(**cleaned_card)
        cleaned_card = validated_schema.model_dump()
    except ValidationError as ve:
        for err in ve.errors():
            loc = " -> ".join(str(x) for x in err["loc"])
            errors.append(f"Schema Validation Error at [{loc}]: {err['msg']}")
    except Exception as e:
        errors.append(f"Schema instantiation failure: {e}")

    is_valid = len(errors) == 0
    return is_valid, cleaned_card, errors

if __name__ == "__main__":
    sample_broken = {
        "id": "abc123ef",
        "deck": "Test::Deck::Path",
        "template": "T1_Cloze",
        "metadata": {
            "difficulty": "beginner",
            "pillar": "01_Cloud_and_Infrastructure",
            "tags": ["test"]
        },
        "content": {
            "scenario": "Broken Cloze ⚡",
            "text": "The algorithm uses {{c1::gradient descent} to optimize.",
            "explanation": "Test explanation.",
            "spanish": "Test spanish."
        }
    }

    valid, fixed, errs = sanitize_and_validate_card(sample_broken)
    print(f"Valid: {valid}")
    print(f"Errors: {errs}")
    print(f"Fixed Card: {json.dumps(fixed, indent=2)}")
