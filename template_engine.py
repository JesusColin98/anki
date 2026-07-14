#!/usr/bin/env python3
"""Multi-Template Engine for Anki Flashcards.

Implements 11 specialized Wozniak-aligned card templates:
- T1:  Atomic Cloze Deletion
- T2:  Dual-Coding Mermaid / Visual
- T3:  Code Snippet & Algorithmic Pattern
- T4:  Scenario & Soft Skills Dialogue
- T5:  MathJax Formula & Physical Law
- T6:  Active Recall Multiple Choice Quiz
- T7:  Pronunciation Drill (Connected Speech) — upgraded with audio_links
- T8:  Minimal Pair Discrimination (Phoneme Demagnetization - Kuhl method)
- T9:  Listening Chunk (Arguelles micro-dictation, gap-fill from native audio)
- T10: Reading Pattern Drill (grapheme-to-phoneme, language-specific)
- T11: Executive Pitch (leadership communication shadowing)
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
        "description": "Pronunciation drills with connected speech rules (audio_links optional)",
        "required_fields": [
            "deck",
            "rule_name",
            "formal_phrase",
            "fast_pronunciation",
            "explanation",
            "spanish",
        ],
    },
    "T8_MinimalPair": {
        "description": "Phoneme discrimination drill — Kuhl Perceptual Magnet demagnetization",
        "required_fields": [
            "deck",
            "phoneme_a",
            "phoneme_b",
            "ipa_a",
            "ipa_b",
            "word_pairs",
            "muscle_tip",
            "language",
        ],
    },
    "T9_ListeningChunk": {
        "description": "Connected-speech listening drill — Arguelles micro-dictation gap-fill",
        "required_fields": [
            "deck",
            "full_transcript",
            "connected_form",
            "gap_text",
            "rules_applied",
            "language",
        ],
    },
    "T10_ReadingPatternDrill": {
        "description": "Grapheme-to-phoneme reading pattern drill, language-specific",
        "required_fields": [
            "deck",
            "language",
            "script_note",
            "grapheme_pattern",
            "word_examples",
            "phoneme_target",
        ],
    },
    "T11_ExecutivePitch": {
        "description": "Leadership communication shadowing — pitch contour and pause analysis",
        "required_fields": [
            "deck",
            "speaker",
            "source_context",
            "transcript_excerpt",
            "pitch_analysis",
            "pause_map",
            "shadowing_script",
            "leadership_technique",
        ],
    },
    "T12_SpeakingPractice": {
        "description": "Speaking practice card with reference audio and a recorder companion link",
        "required_fields": [
            "deck",
            "prompt",
            "scenario",
            "explanation",
            "usage",
            "spanish",
            "model_audio_url",
            "practice_url",
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
    """T7: Pronunciation drill with optional audio links."""
    audio_links = data.get("audio_links", {})
    audio_html = ""
    if audio_links:
        links_html = " &nbsp;|&nbsp; ".join(
            f'<a href="{url}" target="_blank">🔊 {label}</a>'
            for label, url in audio_links.items()
        )
        audio_html = f"<br><br><b>Audio:</b> {links_html}"
    return {
        "deck": data["deck"],
        "scenario": f"Pronunciation Drill: {data['rule_name']} 🗣️",
        "text": (
            f"Practice saying this phrase fast: \"<b>{data['formal_phrase']}</b>\""
            f"<br>Connected speech pronunciation: {{{{c1::{data['fast_pronunciation']}}}}}"
        ),
        "explanation": (
            f"Applied Rule: <b>{data['rule_name']}</b><br>{data['explanation']}"
            f"{audio_html}"
        ),
        "usage": (
            f"Formal: <code>{data['formal_phrase']}</code>"
            f" &rarr; Connected: <code>{data['fast_pronunciation']}</code>"
            f"{audio_html}"
        ),
        "spanish": data["spanish"],
        "audio_links": audio_links,
        "tags": data.get(
            "tags",
            ["pronunciation_drill", data["rule_name"].lower().replace(" ", "_")],
        ),
    }


def render_t8_minimal_pair(data: Dict[str, Any]) -> Dict[str, Any]:
    """T8: Phoneme discrimination drill for Kuhl Perceptual Magnet demagnetization.

    Card front: phoneme symbol + IPA + Forvo audio link
    Card back: full minimal pair list + articulatory tip in Spanish
    """
    audio_links = data.get("audio_links", {})
    forvo_a = audio_links.get("phoneme_a", "http://www.ipachart.com/")
    forvo_b = audio_links.get("phoneme_b", "http://www.ipachart.com/")

    # Build pairs table HTML
    pairs_rows = "".join(
        f"<tr>"
        f"<td><a href='{forvo_a}' target='_blank'>🔊</a> <b>{pair[0]}</b></td>"
        f"<td><code>{pair[2] if len(pair) > 2 else ''}</code></td>"
        f"<td><b>{pair[1]}</b></td>"
        f"<td><code>{pair[3] if len(pair) > 3 else ''}</code></td>"
        f"</tr>"
        for pair in data["word_pairs"]
    )
    pairs_table = (
        "<table border='1' cellpadding='4'>"
        "<thead><tr>"
        f"<th>Word ({data['phoneme_a']})</th><th>IPA</th>"
        f"<th>Word ({data['phoneme_b']})</th><th>IPA</th>"
        "</tr></thead>"
        f"<tbody>{pairs_rows}</tbody></table>"
    )

    return {
        "deck": data["deck"],
        "scenario": f"Minimal Pair 🎯: {data['phoneme_a']} vs {data['phoneme_b']} ({data['language'].upper()})",
        "text": (
            f"<b>Identify the phoneme:</b><br>"
            f"<a href='{forvo_a}' target='_blank'>🔊 {data['phoneme_a']}</a>"
            f" vs "
            f"<a href='{forvo_b}' target='_blank'>🔊 {data['phoneme_b']}</a>"
            f"<br><br>First phoneme IPA: {{{{c1::{data['ipa_a']}}}}}"
        ),
        "explanation": (
            f"<b>Phoneme A:</b> {data['phoneme_a']} — IPA: <code>{data['ipa_a']}</code><br>"
            f"<b>Phoneme B:</b> {data['phoneme_b']} — IPA: <code>{data['ipa_b']}</code><br><br>"
            f"<b>Articulatory Tip (ES):</b> {data['muscle_tip']}<br><br>"
            f"{pairs_table}"
        ),
        "usage": pairs_table,
        "spanish": data["muscle_tip"],
        "audio_links": audio_links,
        "tags": data.get(
            "tags",
            ["minimal_pair", "phonetics", data["language"].lower(),
             data["phoneme_a"].strip("/[]").replace("ː", "_long"),
             data["phoneme_b"].strip("/[]").replace("ː", "_long")],
        ),
    }


def render_t9_listening_chunk(data: Dict[str, Any]) -> Dict[str, Any]:
    """T9: Connected-speech listening drill — Arguelles micro-dictation gap-fill.

    Card front: audio link + gap_text (cloze)
    Card back: full transcript + phonetic rendering + rules applied
    """
    audio_links = data.get("audio_links", {})
    youglish_url = audio_links.get("youglish_phrase", "")
    forvo_url = audio_links.get("forvo_word", "")

    audio_html = ""
    if youglish_url:
        audio_html += f'<a href="{youglish_url}" target="_blank">🎧 YouGlish: Hear in context</a>'
    if forvo_url:
        audio_html += f' &nbsp;|&nbsp; <a href="{forvo_url}" target="_blank">🔊 Forvo: Isolated word</a>'

    rules_list = "".join(
        f"<li><code>{rule}</code></li>" for rule in data.get("rules_applied", [])
    )

    return {
        "deck": data["deck"],
        "scenario": f"Listening Chunk 🎧: {data.get('pattern_name', 'Connected Speech')} ({data['language'].upper()})",
        "text": (
            f"{audio_html}<br><br>"
            f"<b>Fill the gap:</b><br>{data['gap_text']}"
        ),
        "explanation": (
            f"<b>Full transcript:</b> {data['full_transcript']}<br><br>"
            f"<b>Connected form:</b> <i>{data['connected_form']}</i><br><br>"
            f"<b>Phonetic rules applied:</b><ul>{rules_list}</ul>"
        ),
        "usage": (
            f"Native: <code>{data['connected_form']}</code><br>"
            f"Formal: <code>{data['full_transcript']}</code><br>"
            f"{audio_html}"
        ),
        "spanish": data.get("spanish", f"Pronunciación conectada: {data['connected_form']}"),
        "audio_links": audio_links,
        "tags": data.get(
            "tags",
            ["listening", "connected_speech", "micro_dictation", data["language"].lower()]
            + [r.lower().replace(" ", "_") for r in data.get("rules_applied", [])],
        ),
    }


def render_t10_reading_pattern(data: Dict[str, Any]) -> Dict[str, Any]:
    """T10: Grapheme-to-phoneme reading pattern drill, language-specific.

    Card front: grapheme spelling rule → user produces IPA
    Card back: IPA target + 20-30 example words + exceptions
    """
    audio_links = data.get("audio_links", {})

    # Build word list HTML with Forvo audio links
    examples = data.get("word_examples", [])
    example_items = "".join(
        f"<li><b>{word}</b>"
        + (f" — <a href='{audio_links.get(word, forvo_fallback(word, data["language"]))}' target='_blank'>🔊</a>" if True else "")
        + "</li>"
        for word in examples
    )
    example_html = f"<ol>{example_items}</ol>"

    exceptions = data.get("exception_words", [])
    exception_html = ""
    if exceptions:
        exc_items = "".join(f"<li>{w}</li>" for w in exceptions)
        exception_html = f"<br><b>⚠️ Exceptions:</b><ul>{exc_items}</ul>"

    return {
        "deck": data["deck"],
        "scenario": f"Reading Pattern 📖: '{data['grapheme_pattern']}' ({data['language'].upper()} · {data['script_note']})",
        "text": (
            f"<b>Reading rule:</b> <code>{data['grapheme_pattern']}</code><br><br>"
            f"This pattern is pronounced: {{{{c1::{data['phoneme_target']}}}}}"
        ),
        "explanation": (
            f"<b>Grapheme:</b> <code>{data['grapheme_pattern']}</code>"
            f" → <b>Phoneme:</b> <code>{data['phoneme_target']}</code><br><br>"
            f"<b>Examples ({len(examples)} words):</b>{example_html}"
            f"{exception_html}"
        ),
        "usage": example_html + exception_html,
        "spanish": data.get("spanish", f"Patrón de lectura: {data['grapheme_pattern']} → {data['phoneme_target']}"),
        "audio_links": audio_links,
        "tags": data.get(
            "tags",
            ["reading_pattern", "phonics", data["language"].lower(), data["script_note"].lower()],
        ),
    }


def forvo_fallback(word: str, lang_code: str = "en") -> str:
    """Generates a Forvo fallback URL for a word (used in T10 rendering)."""
    from urllib.parse import quote
    return f"https://forvo.com/word/{quote(word.lower(), safe='')}/#en"


def render_t12_speaking_practice(data: Dict[str, Any]) -> Dict[str, Any]:
    """T12: Speaking practice card with remote model audio and a recorder companion link."""
    audio_url = data.get("model_audio_url") or data.get("audio_url", "")
    practice_url = data.get("practice_url", "")
    audio_html = ""
    if audio_url:
        audio_html = (
            f'<div class="audio-player"><audio controls preload="none">'
            f'<source src="{audio_url}" type="audio/mpeg">'
            f'Your browser does not support the audio element.</audio></div>'
        )
    practice_link = ""
    if practice_url:
        practice_link = (
            f'<div class="practice-link"><a href="{practice_url}" target="_blank">🎙️ Open speaking recorder</a></div>'
        )

    return {
        "deck": data["deck"],
        "scenario": data.get("scenario", "Speaking Practice 🎤"),
        "text": (
            f"<b>Prompt:</b> {data['prompt']}<br><br>"
            f"{audio_html}"
        ),
        "explanation": (
            f"{data['explanation']}<br><br>"
            f"<b>Practice tip:</b> {data.get('usage', 'Record yourself and compare your rhythm and intonation with the sample audio.')}"
            f"{practice_link}"
        ),
        "usage": data.get("usage", "Speak naturally and record yourself to compare your delivery."),
        "spanish": data["spanish"],
        "audio": audio_html,
        "practice_link": practice_link,
        "tags": data.get("tags", ["speaking", "pronunciation", "self_recording"]),
        "model_name": "Engaging_Speaking_Model",
    }


def render_t11_executive_pitch(data: Dict[str, Any]) -> Dict[str, Any]:
    """T11: Leadership communication shadowing — pitch contour and pause analysis.

    Card front: transcript excerpt → shadow aloud, identify leadership technique
    Card back: pitch analysis + pause map + shadowing script + technique name
    """
    audio_links = data.get("audio_links", {})
    youglish_url = audio_links.get("youglish_phrase", "")
    yt_url = audio_links.get("youtube_source", "")

    audio_html = ""
    if yt_url:
        audio_html += f'<a href="{yt_url}" target="_blank">▶️ Watch Original</a>'
    if youglish_url:
        sep = " &nbsp;|&nbsp; " if audio_html else ""
        audio_html += f'{sep}<a href="{youglish_url}" target="_blank">🎧 YouGlish Context</a>'

    pitch_labels = {
        "falling": "📉 Falling",
        "rising": "📈 Rising",
        "fall-rise": "📉📈 Fall-Rise",
    }
    pitch_display = pitch_labels.get(
        data.get("pitch_type", ""), data.get("pitch_analysis", "")
    )

    return {
        "deck": data["deck"],
        "scenario": f"Executive Pitch 🎤: {data['speaker']} — {data['source_context']}",
        "text": (
            f"{audio_html}<br><br>"
            f"<b>Shadow this aloud:</b><br>"
            f"<blockquote><i>\"{data['transcript_excerpt']}\"</i></blockquote>"
            f"<br>Which leadership communication technique is used? {{{{c1::{data['leadership_technique']}}}}}"
        ),
        "explanation": (
            f"<b>Speaker:</b> {data['speaker']}<br>"
            f"<b>Context:</b> {data['source_context']}<br><br>"
            f"<b>Pitch Contour:</b> {pitch_display}<br>"
            f"<b>Pause Map:</b> {data['pause_map']}<br><br>"
            f"<b>Shadowing Script (IPA/phonetic):</b><br>"
            f"<code>{data['shadowing_script']}</code><br><br>"
            f"<b>Technique:</b> <b>{data['leadership_technique']}</b>"
        ),
        "usage": (
            f"<b>Original:</b> \"{data['transcript_excerpt']}\"<br>"
            f"<b>Shadow as:</b> <code>{data['shadowing_script']}</code><br>"
            f"{audio_html}"
        ),
        "spanish": data.get(
            "spanish",
            f"Técnica de comunicación ejecutiva: {data['leadership_technique']}",
        ),
        "audio_links": audio_links,
        "tags": data.get(
            "tags",
            [
                "executive_pitch",
                "leadership",
                "shadowing",
                "phonetics",
                data["leadership_technique"].lower().replace(" ", "_").replace("-", "_"),
            ],
        ),
    }


from card_validator import sanitize_and_validate_card

# Renderer dispatch table — maps template name to render function
_RENDERERS = {
    "T1_Cloze": render_t1_cloze,
    "T2_DualCoding": render_t2_dualcoding,
    "T3_CodeSnippet": render_t3_codesnippet,
    "T4_Scenario": render_t4_scenario,
    "T5_MathJax": render_t5_mathjax,
    "T6_Quiz": render_t6_quiz,
    "T7_Pronunciation": render_t7_pronunciation,
    "T8_MinimalPair": render_t8_minimal_pair,
    "T9_ListeningChunk": render_t9_listening_chunk,
    "T10_ReadingPatternDrill": render_t10_reading_pattern,
    "T11_ExecutivePitch": render_t11_executive_pitch,
    "T12_SpeakingPractice": render_t12_speaking_practice,
}


def build_card(template_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Constructs and deterministically validates an Anki card matching template_type.

    Args:
        template_type: One of T1_Cloze through T11_ExecutivePitch.
        data: Dict of card fields. Must include all required_fields for the template.

    Returns:
        A validated, sanitized card dict ready for AnkiConnect import.

    Raises:
        ValueError: If template_type is unknown or required fields are missing.
    """
    if template_type not in TEMPLATES:
        raise ValueError(
            f"Unknown template: {template_type}. "
            f"Valid options: {list(TEMPLATES.keys())}"
        )

    reqs = TEMPLATES[template_type]["required_fields"]
    missing = [f for f in reqs if f not in data]
    if missing:
        raise ValueError(f"Missing required fields for {template_type}: {missing}")

    renderer = _RENDERERS[template_type]
    raw_card = renderer(data)

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
