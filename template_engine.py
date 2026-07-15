#!/usr/bin/env python3
"""Multi-Template Engine for Anki Flashcards.

Implements 16 specialized Wozniak-aligned card templates:
- T1:  Atomic Cloze Deletion
- T2:  Dual-Coding Mermaid / Visual
- T3:  Code Snippet & Algorithmic Pattern
- T4:  Scenario & Soft Skills Dialogue
- T5:  MathJax Formula & Physical Law
- T6:  Active Recall Multiple Choice Quiz
- T7:  Pronunciation Drill (Connected Speech)
- T8:  Minimal Pair Discrimination
- T9:  Listening Chunk (Arguelles micro-dictation)
- T10: Reading Pattern Drill
- T11: Executive Pitch
- T12: Speaking Practice
- T13: Mnemonic Palace
- T14: Peg Number
- T15A: Feynman Analogy
- T15B: Feynman Scenario
- T16: Name-Face
"""

import json
import random
import hashlib
from typing import Any, Dict, List

TEMPLATES = {
    "T1_Cloze": {
        "description": "Atomic Cloze Deletion for vocabulary and core facts",
        "required_fields": ["deck", "text", "explanation", "spanish"],
    },
    "T2_DualCoding": {
        "description": "Dual-Coding visual representation with Mermaid graph",
        "required_fields": ["deck", "concept", "mermaid_code", "explanation", "spanish"],
    },
    "T3_CodeSnippet": {
        "description": "Code patterns, algorithms, and CLI commands",
        "required_fields": ["deck", "title", "code_block", "language", "explanation"],
    },
    "T4_Scenario": {
        "description": "Real-world professional scenarios & negotiation",
        "required_fields": ["deck", "scenario", "target_phrase", "usage", "spanish"],
    },
    "T5_MathJax": {
        "description": "LaTeX/MathJax formulas and physical laws",
        "required_fields": ["deck", "concept", "formula_latex", "variable_breakdown"],
    },
    "T6_Quiz": {
        "description": "Active recall quiz with multiple choice options",
        "required_fields": ["deck", "question", "options", "correct_option", "rationale"],
    },
    "T7_Pronunciation": {
        "description": "Connected speech pronunciation drills",
        "required_fields": ["deck", "rule_name", "formal_phrase", "fast_pronunciation", "explanation", "spanish"],
    },
    "T8_MinimalPair": {
        "description": "Phoneme discrimination drill",
        "required_fields": ["deck", "phoneme_a", "phoneme_b", "ipa_a", "ipa_b", "word_pairs", "muscle_tip", "language"],
    },
    "T9_ListeningChunk": {
        "description": "Listening chunk Arguelles micro-dictation gap-fill",
        "required_fields": ["deck", "full_transcript", "connected_form", "gap_text", "rules_applied", "language"],
    },
    "T10_ReadingPatternDrill": {
        "description": "Grapheme-to-phoneme reading pattern drill",
        "required_fields": ["deck", "language", "script_note", "grapheme_pattern", "word_examples", "phoneme_target"],
    },
    "T11_ExecutivePitch": {
        "description": "Leadership communication shadowing",
        "required_fields": ["deck", "speaker", "source_context", "transcript_excerpt", "pitch_analysis", "pause_map", "shadowing_script", "leadership_technique"],
    },
    "T12_SpeakingPractice": {
        "description": "Speaking practice card with reference audio and recorder link",
        "required_fields": ["deck", "prompt", "explanation", "usage", "spanish", "model_audio_url", "practice_url"],
    },
    "T13_MnemonicPalace": {
        "description": "Mnemonic Palace anchoring for concepts",
        "required_fields": ["deck", "concept", "explanation", "spanish", "palace_name", "locus_stop", "mnemonic_scene"],
    },
    "T14_PegNumber": {
        "description": "Peg System number association",
        "required_fields": ["deck", "concept", "number", "phonetic_code", "peg_word", "visual_scene"],
    },
    "T15A_FeynmanAnalogy": {
        "description": "Feynman Method layperson analogy",
        "required_fields": ["deck", "concept", "layperson_explanation", "metaphor_analogy", "explanation"],
    },
    "T15B_FeynmanScenario": {
        "description": "Feynman Method scenario application challenge",
        "required_fields": ["deck", "concept", "generation_challenge", "explanation"],
    },
    "T16_NameFace": {
        "description": "Name-to-Face and context recognition",
        "required_fields": ["deck", "person_name", "distinguishing_feature", "substitute_word_or_image", "association_scene", "contribution"],
    },
}

# ===========================================================================
# INTERACTIVE LAYOUT BUILDERS (TABS & MATCH GAME)
# ===========================================================================

def build_tabs(tabs: Dict[str, str], card_id: str = "") -> str:
    """Generates HTML/JS tabs with sessionStorage state persistence."""
    random_id = f"{random.randint(0, 1000000)}"
    headers = []
    contents = []
    
    # Generate tab buttons and contents
    for i, (title, content) in enumerate(tabs.items()):
        active_class = " active" if i == 0 else ""
        tab_id = f"tab_{random_id}_{i}"
        headers.append(f'<button class="tab-btn{active_class}" data-tab-name="{title}" onclick="switchTab(event, \'{tab_id}\')">{title}</button>')
        contents.append(f'<div id="{tab_id}" class="tab-content{active_class}">{content}</div>')
        
    headers_html = "\n".join(headers)
    contents_html = "\n".join(contents)
    
    js_script = f"""
<script>
(function() {{
  const cardId = "{card_id}";
  
  if (typeof window.switchTab !== 'function') {{
    window.switchTab = function(evt, tabId) {{
      var parent = evt.currentTarget.closest('.tabs-container');
      var contents = parent.getElementsByClassName("tab-content");
      for (var i = 0; i < contents.length; i++) {{
        contents[i].classList.remove("active");
      }}
      var buttons = parent.getElementsByClassName("tab-btn");
      for (var i = 0; i < buttons.length; i++) {{
        buttons[i].classList.remove("active");
      }}
      document.getElementById(tabId).classList.add("active");
      evt.currentTarget.classList.add("active");
      
      // Persist active tab name to sessionStorage
      var tabName = evt.currentTarget.getAttribute("data-tab-name");
      if (cardId && tabName) {{
        sessionStorage.setItem("active_tab_" + cardId, tabName);
      }}
    }};
  }}
  
  // Restore tab state on load
  if (cardId) {{
    var savedTabName = sessionStorage.getItem("active_tab_" + cardId);
    if (savedTabName) {{
      var container = document.querySelector('[data-card-id="' + cardId + '"]');
      if (container) {{
        var btn = Array.from(container.querySelectorAll(".tab-btn")).find(b => b.getAttribute("data-tab-name") === savedTabName);
        if (btn) {{
          // Temporarily disable transition during auto-click to avoid layout shift
          btn.click();
        }}
      }}
    }}
  }}
}})();
</script>
"""
    return f"""
<div class="tabs-container" data-card-id="{card_id}">
  <div class="tabs-header">
    {headers_html}
  </div>
  {contents_html}
</div>
{js_script}
"""

def build_match_game(match_data: Dict[str, Any]) -> str:
    """Creates a gamified terms matching game directly in the card DOM."""
    pairs = match_data.get("pairs", [])
    if not pairs:
        return ""
        
    game_id = f"mg_{random.randint(0, 1000000)}"
    terms = [p["term"] for p in pairs]
    meanings = [p["meaning"] for p in pairs]
    
    # Shuffle for presentation
    shuffled_terms = sorted(terms, key=lambda x: random.random())
    shuffled_meanings = sorted(meanings, key=lambda x: random.random())
    
    terms_html = "\n".join(f'<div class="mg-item term-item" data-term="{t}">{t}</div>' for t in shuffled_terms)
    meanings_html = "\n".join(f'<div class="mg-item meaning-item" data-meaning="{m}">{m}</div>' for m in shuffled_meanings)
    
    game_html = f"""
<div class="match-game" id="{game_id}">
  <div class="column terms-column">
    <h4>Conceptos</h4>
    {terms_html}
  </div>
  <div class="column meanings-column">
    <h4>Significados</h4>
    {meanings_html}
  </div>
</div>
<script>
(function() {{
  const container = document.getElementById("{game_id}");
  const pairs = {json.dumps(pairs)};
  let selectedTerm = null;
  let selectedMeaning = null;
  let matchesCount = 0;

  const termItems = container.querySelectorAll(".term-item");
  const meaningItems = container.querySelectorAll(".meaning-item");

  termItems.forEach(item => {{
    item.addEventListener("click", () => {{
      if (item.classList.contains("matched")) return;
      termItems.forEach(i => i.classList.remove("selected"));
      item.classList.add("selected");
      selectedTerm = item;
      checkMatch();
    }});
  }});

  meaningItems.forEach(item => {{
    item.addEventListener("click", () => {{
      if (item.classList.contains("matched")) return;
      meaningItems.forEach(i => i.classList.remove("selected"));
      item.classList.add("selected");
      selectedMeaning = item;
      checkMatch();
    }});
  }});

  function checkMatch() {{
    if (!selectedTerm || !selectedMeaning) return;
    const termVal = selectedTerm.getAttribute("data-term");
    const meaningVal = selectedMeaning.getAttribute("data-meaning");

    const pair = pairs.find(p => p.term === termVal && p.meaning === meaningVal);
    if (pair) {{
      selectedTerm.classList.remove("selected");
      selectedMeaning.classList.remove("selected");
      selectedTerm.classList.add("matched", "success");
      selectedMeaning.classList.add("matched", "success");
      selectedTerm = null;
      selectedMeaning = null;
      matchesCount++;
      if (matchesCount === pairs.length) {{
        const successBanner = document.createElement("div");
        successBanner.className = "mg-success-banner";
        successBanner.innerHTML = "🎉 ¡Felicidades! Todos combinados correctamente.";
        container.appendChild(successBanner);
      }}
    }} else {{
      const t = selectedTerm;
      const m = selectedMeaning;
      t.classList.add("mismatch");
      m.classList.add("mismatch");
      selectedTerm = null;
      selectedMeaning = null;
      setTimeout(() => {{
        t.classList.remove("selected", "mismatch");
        m.classList.remove("selected", "mismatch");
      }}, 600);
    }}
  }}
}})();
</script>
"""
    return game_html

# ===========================================================================
# TEMPLATE RENDER FUNCTIONS
# ===========================================================================

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
    mermaid_html = f"""<div class="mermaid">\n{data['mermaid_code']}\n</div>"""
    return {
        "deck": data["deck"],
        "scenario": f"Dual-Coding Diagram 📊 ({data['concept']})",
        "text": f"¿Cómo funciona la estructura de {{{{c1::{data['concept']}}}}} en el sistema?",
        "explanation": f"{data['explanation']}<br><br>{mermaid_html}",
        "usage": f"Visual model for <code>{data['concept']}</code>.<br>Graph: {mermaid_html}",
        "spanish": data["spanish"],
        "tags": data.get("tags", ["wozniak_t2_dualcoding"]),
    }

def render_t3_codesnippet(data: Dict[str, Any]) -> Dict[str, Any]:
    lang = data.get("language", "python")
    code_formatted = f'<pre><code class="language-{lang}">{data["code_block"]}</code></pre>'
    return {
        "deck": data["deck"],
        "scenario": f"Code Pattern 💻 ({data['title']})",
        "text": f"Patrón de código en <b>{lang}</b> para {{{{c1::{data['title']}}}}}:<br>{code_formatted}",
        "explanation": data["explanation"],
        "usage": f"Snippet: {code_formatted}<br>Output expected: <code>{data.get('expected_output', 'Success')}</code>",
        "spanish": f"Patrón de código: {data['title']}",
        "tags": data.get("tags", ["wozniak_t3_codesnippet", lang]),
    }

def render_t4_scenario(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "deck": data["deck"],
        "scenario": data["scenario"],
        "text": f"In this situation, you should say: \"{{c1::{data['target_phrase']}}}\"",
        "explanation": data.get("explanation", f"Professional phrase for: {data['scenario']}"),
        "usage": data["usage"],
        "spanish": data["spanish"],
        "tags": data.get("tags", ["wozniak_t4_scenario"]),
    }

def render_t5_mathjax(data: Dict[str, Any]) -> Dict[str, Any]:
    formula = data["formula_latex"]
    return {
        "deck": data["deck"],
        "scenario": f"Math & Physics 📐 ({data['concept']})",
        "text": f"Ecuación para {{{{c1::{data['concept']}}}}}: \\[{formula}\\]",
        "explanation": f"Desglose de variables: <ul>{data['variable_breakdown']}</ul>",
        "usage": f"Formula: \\[{formula}\\]",
        "spanish": f"Fórmula de {data['concept']}",
        "tags": data.get("tags", ["wozniak_t5_mathjax"]),
    }

def render_t6_quiz(data: Dict[str, Any]) -> Dict[str, Any]:
    options_html = "".join([f"<li>{opt}</li>" for opt in data["options"]])
    return {
        "deck": data["deck"],
        "scenario": "Active Recall Quiz 🎯",
        "text": f"<b>Pregunta:</b> {data['question']}<br>Opciones:<ul>{options_html}</ul><br>Respuesta correcta: {{{{c1::{data['correct_option']}}}}}",
        "explanation": f"Justificación: {data['rationale']}",
        "usage": f"Quiz assertion: {data['correct_option']}",
        "spanish": f"Quiz: {data['question']}",
        "tags": data.get("tags", ["wozniak_t6_quiz"]),
    }

def render_t7_pronunciation(data: Dict[str, Any]) -> Dict[str, Any]:
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
        "text": f"Practice saying this phrase fast: \"<b>{data['formal_phrase']}</b>\"<br>Connected speech pronunciation: {{{{c1::{data['fast_pronunciation']}}}}}",
        "explanation": f"Applied Rule: <b>{data['rule_name']}</b><br>{data['explanation']}{audio_html}",
        "usage": f"Formal: <code>{data['formal_phrase']}</code> &rarr; Connected: <code>{data['fast_pronunciation']}</code>{audio_html}",
        "spanish": data["spanish"],
        "audio_links": audio_links,
        "tags": data.get("tags", ["pronunciation_drill", data["rule_name"].lower().replace(" ", "_")]),
    }

def render_t8_minimal_pair(data: Dict[str, Any]) -> Dict[str, Any]:
    audio_links = data.get("audio_links", {})
    forvo_a = audio_links.get("phoneme_a", "http://www.ipachart.com/")
    forvo_b = audio_links.get("phoneme_b", "http://www.ipachart.com/")
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
            f"<a href='{forvo_a}' target='_blank'>🔊 {data['phoneme_a']}</a> vs <a href='{forvo_b}' target='_blank'>🔊 {data['phoneme_b']}</a>"
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
        "tags": data.get("tags", ["minimal_pair", "phonetics", data["language"].lower()]),
    }

def render_t9_listening_chunk(data: Dict[str, Any]) -> Dict[str, Any]:
    audio_links = data.get("audio_links", {})
    youglish_url = audio_links.get("youglish_phrase", "")
    forvo_url = audio_links.get("forvo_word", "")
    audio_html = ""
    if youglish_url:
        audio_html += f'<a href="{youglish_url}" target="_blank">🎧 YouGlish: Hear in context</a>'
    if forvo_url:
        audio_html += f' &nbsp;|&nbsp; <a href="{forvo_url}" target="_blank">🔊 Forvo: Isolated word</a>'
    rules_list = "".join(f"<li><code>{rule}</code></li>" for rule in data.get("rules_applied", []))
    return {
        "deck": data["deck"],
        "scenario": f"Listening Chunk 🎧: {data.get('pattern_name', 'Connected Speech')} ({data['language'].upper()})",
        "text": f"{audio_html}<br><br><b>Fill the gap:</b><br>{data['gap_text']}",
        "explanation": (
            f"<b>Full transcript:</b> {data['full_transcript']}<br><br>"
            f"<b>Connected form:</b> <i>{data['connected_form']}</i><br><br>"
            f"<b>Phonetic rules applied:</b><ul>{rules_list}</ul>"
        ),
        "usage": f"Native: <code>{data['connected_form']}</code><br>Formal: <code>{data['full_transcript']}</code><br>{audio_html}",
        "spanish": data.get("spanish", f"Connected speech: {data['connected_form']}"),
        "audio_links": audio_links,
        "tags": data.get("tags", ["listening", "connected_speech", "micro_dictation", data["language"].lower()]),
    }

def render_t10_reading_pattern(data: Dict[str, Any]) -> Dict[str, Any]:
    audio_links = data.get("audio_links", {})
    examples = data.get("word_examples", [])
    example_items = "".join(
        f"<li><b>{word}</b> — <a href='{audio_links.get(word, 'https://forvo.com/word/' + word + '/#en')}' target='_blank'>🔊</a></li>"
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
        "text": f"<b>Reading rule:</b> <code>{data['grapheme_pattern']}</code><br><br>This pattern is pronounced: {{{{c1::{data['phoneme_target']}}}}}",
        "explanation": (
            f"<b>Grapheme:</b> <code>{data['grapheme_pattern']}</code> → <b>Phoneme:</b> <code>{data['phoneme_target']}</code><br><br>"
            f"<b>Examples ({len(examples)} words):</b>{example_html}{exception_html}"
        ),
        "usage": example_html + exception_html,
        "spanish": data.get("spanish", f"Reading pattern: {data['grapheme_pattern']} → {data['phoneme_target']}"),
        "audio_links": audio_links,
        "tags": data.get("tags", ["reading_pattern", "phonics", data["language"].lower()]),
    }

def render_t11_executive_pitch(data: Dict[str, Any]) -> Dict[str, Any]:
    audio_links = data.get("audio_links", {})
    yt_url = audio_links.get("youtube_source", "")
    youglish_url = audio_links.get("youglish_phrase", "")
    audio_html = ""
    if yt_url:
        audio_html += f'<a href="{yt_url}" target="_blank">▶️ Watch Original</a>'
    if youglish_url:
        sep = " &nbsp;|&nbsp; " if audio_html else ""
        audio_html += f'{sep}<a href="{youglish_url}" target="_blank">🎧 YouGlish Context</a>'
    return {
        "deck": data["deck"],
        "scenario": f"Executive Pitch 🎤: {data['speaker']} — {data['source_context']}",
        "text": (
            f"{audio_html}<br><br><b>Shadow this aloud:</b><br>"
            f"<blockquote><i>\"{data['transcript_excerpt']}\"</i></blockquote><br>"
            f"Which leadership communication technique is used? {{{{c1::{data['leadership_technique']}}}}}"
        ),
        "explanation": (
            f"<b>Speaker:</b> {data['speaker']}<br><b>Context:</b> {data['source_context']}<br><br>"
            f"<b>Pitch Contour:</b> {data['pitch_analysis']}<br><b>Pause Map:</b> {data['pause_map']}<br><br>"
            f"<b>Shadowing Script:</b><br><code>{data['shadowing_script']}</code><br><br>"
            f"<b>Technique:</b> <b>{data['leadership_technique']}</b>"
        ),
        "usage": f"Original: \"{data['transcript_excerpt']}\"<br>Shadow: <code>{data['shadowing_script']}</code><br>{audio_html}",
        "spanish": data.get("spanish", f"Technique: {data['leadership_technique']}"),
        "audio_links": audio_links,
        "tags": data.get("tags", ["executive_pitch", "leadership", "shadowing"]),
    }

def render_t12_speaking_practice(data: Dict[str, Any]) -> Dict[str, Any]:
    audio_url = data.get("model_audio_url", "")
    practice_url = data.get("practice_url", "")
    audio_html = ""
    if audio_url:
        audio_html = (
            f'<div class="audio-player"><audio controls preload="none">'
            f'<source src="{audio_url}" type="audio/mpeg">'
            f'Browser not supported.</audio></div>'
        )
    practice_link = ""
    if practice_url:
        practice_link = f'<div class="practice-link"><a href="{practice_url}" target="_blank">🎙️ Open speaking recorder</a></div>'
    return {
        "deck": data["deck"],
        "scenario": data.get("scenario", "Speaking Practice 🎤"),
        "text": f"<b>Prompt:</b> {data['prompt']}<br><br>{audio_html}",
        "explanation": f"{data['explanation']}<br><br><b>Practice tip:</b> {data.get('usage', 'Record yourself and compare rhythm.')}{practice_link}",
        "usage": data.get("usage", "Record and compare audio."),
        "spanish": data["spanish"],
        "audio": audio_html,
        "practice_link": practice_link,
        "tags": data.get("tags", ["speaking", "pronunciation"]),
    }

def render_t13_mnemonic_palace(data: Dict[str, Any]) -> Dict[str, Any]:
    text_content = (
        f"¿Cómo se asocia el concepto {{{{c1::{data['concept']}}}}} en el Palacio de la Memoria?<br><br>"
        f"<blockquote>🏢 <b>Palacio:</b> {data['palace_name']}<br>📍 <b>Lugar (Locus):</b> {data['locus_stop']}</blockquote>"
    )
    explanation_tabs = build_tabs({
        "Mnemotecnia": f"<b>Escena Visual:</b><br>{data['mnemonic_scene']}",
        "Explicación Técnica": data["explanation"],
        "Traducción (ES)": data["spanish"]
    }, data.get("id", ""))
    return {
        "deck": data["deck"],
        "scenario": f"Mnemonic Palace 🏢 ({data['concept']})",
        "text": text_content,
        "explanation": explanation_tabs,
        "usage": f"Locus: <code>{data['palace_name']} -> {data['locus_stop']}</code>",
        "spanish": data["spanish"],
        "tags": data.get("tags", ["mnemonic_palace", "memory_techniques"]),
    }

def render_t14_peg_number(data: Dict[str, Any]) -> Dict[str, Any]:
    explanation_tabs = build_tabs({
        "Clavija (Peg)": f"<b>Palabra Clave (Peg):</b> {data['peg_word']}<br><b>Código Fonético:</b> <code>{data['phonetic_code']}</code>",
        "Escena Mnemotécnica": data["visual_scene"]
    }, data.get("id", ""))
    return {
        "deck": data["deck"],
        "scenario": f"Peg System 🎯 (Número: {data['number']})",
        "text": f"¿Cuál es la palabra clave / escena para el número {{{{c1::{data['concept']}}}}} (Número: {data['number']})?",
        "explanation": explanation_tabs,
        "usage": f"Number: <code>{data['number']}</code> | Peg: <b>{data['peg_word']}</b>",
        "spanish": f"Número {data['number']} -> Peg {data['peg_word']}",
        "tags": data.get("tags", ["peg_system", "memory_techniques"]),
    }

def render_t15a_feynman_analogy(data: Dict[str, Any]) -> Dict[str, Any]:
    explanation_tabs = build_tabs({
        "Intuición (Simple)": data["layperson_explanation"],
        "Metáfora / Analogía": data["metaphor_analogy"],
        "Detalle Técnico": data["explanation"]
    }, data.get("id", ""))
    return {
        "deck": data["deck"],
        "scenario": f"Feynman Analogy 👶 ({data['concept']})",
        "text": f"¿Cómo se explica con una analogía simple el concepto de {{{{c1::{data['concept']}}}}}?",
        "explanation": explanation_tabs,
        "usage": f"Feynman Analogy for {data['concept']}",
        "spanish": f"Analogía de {data['concept']}",
        "tags": data.get("tags", ["feynman_method", "analogy"]),
    }

def render_t15b_feynman_scenario(data: Dict[str, Any]) -> Dict[str, Any]:
    explanation_tabs = build_tabs({
        "Resolución Técnica": data["explanation"],
        "Desafío Aplicado": data["generation_challenge"]
    }, data.get("id", ""))
    return {
        "deck": data["deck"],
        "scenario": f"Feynman Challenge ⚡ ({data['concept']})",
        "text": (
            f"<b>Feynman Challenge:</b> Aplica {data['concept']} al siguiente escenario:<br>"
            f"<blockquote>{data['generation_challenge']}</blockquote>"
            f"¿Cómo funciona la resolución técnica? {{{{c1::{data['concept']}}}}}"
        ),
        "explanation": explanation_tabs,
        "usage": f"Feynman Challenge for {data['concept']}",
        "spanish": f"Desafío de aplicación: {data['concept']}",
        "tags": data.get("tags", ["feynman_method", "scenario_challenge"]),
    }

def render_t16_name_face(data: Dict[str, Any]) -> Dict[str, Any]:
    explanation_tabs = build_tabs({
        "Asociación": f"<b>Nombre:</b> {data['person_name']}<br><b>Palabra Sustituta/Imagen:</b> {data['substitute_word_or_image']}",
        "Contribución": data["contribution"]
    }, data.get("id", ""))
    return {
        "deck": data["deck"],
        "scenario": f"Name-Face Portrait 👤",
        "text": (
            f"¿Quién es la persona y cuál es su contribución clave?<br><br>"
            f"<blockquote>🎨 <b>Rasgo Distintivo:</b> {data['distinguishing_feature']}<br>🧠 <b>Asociación:</b> {data['association_scene']}</blockquote>"
            f"Nombre: {{{{c1::{data['person_name']}}}}}"
        ),
        "explanation": explanation_tabs,
        "usage": f"Name-Face Portrait for {data['person_name']}",
        "spanish": f"Persona: {data['person_name']}",
        "tags": data.get("tags", ["name_face", "memory_techniques"]),
    }

# ===========================================================================
# DISPATCH & INTEGRATION PIPELINE
# ===========================================================================

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
    "T13_MnemonicPalace": render_t13_mnemonic_palace,
    "T14_PegNumber": render_t14_peg_number,
    "T15A_FeynmanAnalogy": render_t15a_feynman_analogy,
    "T15B_FeynmanScenario": render_t15b_feynman_scenario,
    "T16_NameFace": render_t16_name_face,
}

from card_validator import sanitize_and_validate_card

def build_card(template_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Constructs, decorates, and validates an Anki card matching template_type."""
    if template_type not in TEMPLATES:
        raise ValueError(
            f"Unknown template: {template_type}. "
            f"Valid options: {list(TEMPLATES.keys())}"
        )

    # Validate that we have all required fields (after flattening)
    reqs = TEMPLATES[template_type]["required_fields"]
    missing = [f for f in reqs if f not in data]
    if missing:
        raise ValueError(f"Missing required fields for {template_type}: {missing}")

    renderer = _RENDERERS[template_type]
    raw_card = renderer(data)

    # -------------------------------------------------------------
    # DECORATE CARD WITH DYNAMIC INTERACTIVE COMPONENTS
    # -------------------------------------------------------------
    # 1. Analogy Tab (Elaboration Tabbed Panel)
    if "analogy" in data and data["analogy"] and template_type not in ["T13_MnemonicPalace", "T14_PegNumber", "T15A_FeynmanAnalogy", "T15B_FeynmanScenario", "T16_NameFace"]:
        raw_card["explanation"] = build_tabs({
            "Intuición (Detalle)": raw_card["explanation"],
            "Analogía / Metáfora": data["analogy"]
        }, data.get("id"))

    # 2. Interactive Match Game
    if "match_game_data" in data and data["match_game_data"]:
        game_html = build_match_game(data["match_game_data"])
        if game_html:
            if data.get("difficulty") == "learning":
                raw_card["text"] += "<br><br>" + game_html
            else:
                raw_card["explanation"] += "<br><br>" + game_html

    # 3. Interactive click-to-reveal script for Mermaid Diagrams with index-based sessionStorage
    full_str = json.dumps(raw_card)
    card_id = data.get("id", "")
    if 'class="mermaid"' in full_str:
        js_revealer = f"""
<script>
(function() {{
  var cardId = "{card_id}";
  function setupClozeNodes() {{
    var nodes = document.querySelectorAll('.mermaid .cloze-node');
    if (cardId) {{
      var revealed = JSON.parse(sessionStorage.getItem("revealed_nodes_" + cardId) || "[]");
      nodes.forEach((node, index) => {{
        if (revealed.includes(index)) {{
          node.classList.add('revealed');
        }}
        node.removeEventListener('click', node._revealHandler);
        node._revealHandler = () => {{
          node.classList.toggle('revealed');
          var current = JSON.parse(sessionStorage.getItem("revealed_nodes_" + cardId) || "[]");
          if (node.classList.contains('revealed')) {{
            if (!current.includes(index)) current.push(index);
          }} else {{
            current = current.filter(idx => idx !== index);
          }}
          sessionStorage.setItem("revealed_nodes_" + cardId, JSON.stringify(current));
        }};
        node.addEventListener('click', node._revealHandler);
      }});
    }}
  }}
  setupClozeNodes();
  setTimeout(setupClozeNodes, 200);
  setTimeout(setupClozeNodes, 600);
  setTimeout(setupClozeNodes, 1500);
}})();
</script>
"""
        if "explanation" in raw_card:
            raw_card["explanation"] += js_revealer
        if "usage" in raw_card:
            raw_card["usage"] += js_revealer

    # Ensure structure fields match the Pydantic schema structure
    # Rebuild nested structure
    pydantic_ready = {
        "id": data.get("id", hashlib.sha256(str(data).encode('utf-8')).hexdigest()[:16]),
        "deck": raw_card["deck"],
        "template": template_type,
        "metadata": {
            "difficulty": data.get("difficulty", "intermediate"),
            "pillar": data.get("pillar", raw_card["deck"].split("::")[0]),
            "tags": data.get("tags", raw_card.get("tags", []))
        },
        "content": {
            "scenario": raw_card.get("scenario", "General"),
            "text": raw_card.get("text", ""),
            "explanation": raw_card.get("explanation", ""),
            "spanish": raw_card.get("spanish", ""),
            "usage": raw_card.get("usage", "")
        },
        "mnemonics": {
            "palace_name": data.get("palace_name", ""),
            "locus_stop": data.get("locus_stop", ""),
            "mnemonic_scene": data.get("mnemonic_scene", ""),
            "peg_word": data.get("peg_word", ""),
            "phonetic_code": data.get("phonetic_code", "")
        },
        "interactivity": {
            "analogy": data.get("analogy", ""),
            "interactive_mermaid": data.get("interactive_mermaid", ""),
            "match_game_data": data.get("match_game_data", None)
        }
    }
    
    # Copy any other extra custom fields to content from raw input data
    for k, v in data.items():
        if k not in ["deck", "tags", "difficulty", "pillar", "palace_name", "locus_stop", "mnemonic_scene", "peg_word", "phonetic_code", "analogy", "interactive_mermaid", "match_game_data"]:
            if k not in pydantic_ready["content"]:
                pydantic_ready["content"][k] = v

    # Run deterministic validation & auto-repair pipeline
    is_valid, cleaned_card, validation_errors = sanitize_and_validate_card(pydantic_ready)
    if validation_errors:
        print(f"[!] Deterministic Validator Warning for {template_type}: {validation_errors}")

    return cleaned_card

if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    sample_t13 = {
        "id": "test_mnem_01",
        "deck": "06_Business_and_Productivity::Learning_and_Memory::Methodology::memory_techniques_and_systems",
        "concept": "Loci Method",
        "explanation": "Visual maps in physical locations.",
        "spanish": "Método de Loci",
        "palace_name": "Living Room",
        "locus_stop": "01_TV",
        "mnemonic_scene": "A huge glowing TV displaying a brain.",
        "analogy": "It is like marking coordinates on a map."
    }
    card = build_card("T13_MnemonicPalace", sample_t13)
    print(json.dumps(card, indent=2, ensure_ascii=False))
