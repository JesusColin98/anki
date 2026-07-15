#!/usr/bin/env python3
"""
audit_and_fix.py — Full Data Quality Audit & Auto-Fix Pipeline
===============================================================
Scans every JSON deck file under decks/, validates and repairs cards
in-place using the same sanitizer logic as card_validator.py, and
produces a detailed JSON + Markdown report.

Fix categories applied automatically:
  1. Broken / unclosed Cloze tags  {{c1::text}  →  {{c1::text}}
  2. Invalid Mermaid arrow syntax   ->|...| → -->|...|
  3. Missing 'pillar' in metadata   → inferred from file path
  4. Empty/missing 'spanish' field in T1/T4/T7  → flagged (cannot auto-fill)
  5. Empty 'explanation' < 20 chars  → flagged
  6. Cards with unknown template     → flagged
  7. Unbalanced MathJax delimiters  → flagged (structural, cannot auto-fix)
  8. T14 visual_scene in wrong key  → moved from content to interactivity
  9. Duplicate card IDs within same file → second occurrence gets new UUID suffix
 10. Missing required content fields    → flagged (cannot auto-fill semantic data)
"""

import json
import os
import re
import uuid
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DECKS_ROOT = Path(__file__).parent / "decks"
REPORT_PATH = Path(__file__).parent / "scratch" / "audit_report.json"
MD_REPORT_PATH = Path(__file__).parent / "scratch" / "audit_report.md"

VALID_TEMPLATES = {
    "T1_Cloze", "T2_DualCoding", "T3_CodeSnippet", "T4_Scenario",
    "T5_MathJax", "T6_Quiz", "T7_Pronunciation", "T8_MinimalPair",
    "T9_ListeningChunk", "T10_ReadingPatternDrill", "T11_ExecutivePitch",
    "T12_SpeakingPractice", "T13_MnemonicPalace", "T14_PegNumber",
    "T15A_FeynmanAnalogy", "T15B_FeynmanScenario", "T16_NameFace",
}

REQUIRED_FIELDS: Dict[str, List[str]] = {
    "T1_Cloze":               ["text", "explanation", "spanish"],
    "T2_DualCoding":          ["concept", "mermaid_code", "explanation", "spanish"],
    "T3_CodeSnippet":         ["title", "code_block", "language", "explanation"],
    "T4_Scenario":            ["scenario", "target_phrase", "usage", "spanish"],
    "T5_MathJax":             ["concept", "formula_latex", "variable_breakdown"],
    "T6_Quiz":                ["question", "options", "correct_option", "rationale"],
    "T7_Pronunciation":       ["rule_name", "formal_phrase", "fast_pronunciation", "explanation", "spanish"],
    "T8_MinimalPair":         ["phoneme_a", "phoneme_b", "ipa_a", "ipa_b", "word_pairs", "muscle_tip", "language"],
    "T9_ListeningChunk":      ["full_transcript", "connected_form", "gap_text", "rules_applied", "language"],
    "T10_ReadingPatternDrill":["language", "script_note", "grapheme_pattern", "word_examples", "phoneme_target"],
    "T11_ExecutivePitch":     ["speaker", "source_context", "transcript_excerpt", "pitch_analysis",
                               "pause_map", "shadowing_script", "leadership_technique"],
    "T12_SpeakingPractice":   ["prompt", "explanation", "usage", "spanish", "model_audio_url", "practice_url"],
    "T13_MnemonicPalace":     ["concept", "explanation", "spanish"],
    "T14_PegNumber":          ["concept", "number", "phonetic_code", "peg_word", "visual_scene"],
    "T15A_FeynmanAnalogy":    ["concept", "layperson_explanation", "metaphor_analogy", "explanation"],
    "T15B_FeynmanScenario":   ["concept", "generation_challenge", "explanation"],
    "T16_NameFace":           ["person_name", "distinguishing_feature", "substitute_word_or_image",
                               "association_scene", "contribution"],
}

PILLAR_PREFIXES = {
    "01_Cloud_and_Infrastructure": "01_Cloud_and_Infrastructure",
    "02_AI_and_Data_Science": "02_AI_and_Data_Science",
    "03_Languages": "03_Languages",
    "04_Social_and_Humanities": "04_Social_and_Humanities",
    "05_Soft_Skills_and_Leadership": "05_Soft_Skills_and_Leadership",
    "06_Business_and_Productivity": "06_Business_and_Productivity",
}


# ---------------------------------------------------------------------------
# Repair helpers
# ---------------------------------------------------------------------------

def infer_pillar(json_path: Path) -> Optional[str]:
    """Infer the pillar name from the file path."""
    for part in json_path.parts:
        if part in PILLAR_PREFIXES:
            return PILLAR_PREFIXES[part]
    return None


def repair_cloze(text: str) -> Tuple[str, List[str]]:
    """Fix unclosed single-brace Cloze tags."""
    fixes: List[str] = []
    # {{c1::text} → {{c1::text}}
    repaired = re.sub(r"\{\{(c\d+::[^}]+)\}(?!\})", r"{{\1}}", text)
    if repaired != text:
        fixes.append(f"repaired_cloze: '{text[:80]}' → '{repaired[:80]}'")
    return repaired, fixes


def repair_mermaid(code: str) -> Tuple[str, List[str]]:
    """Repair common Mermaid arrow issues."""
    fixes: List[str] = []
    original = code
    valid_headers = ("graph", "flowchart", "sequenceDiagram", "classDiagram",
                     "stateDiagram", "erDiagram", "gantt")
    stripped = code.strip()
    if not any(stripped.startswith(h) for h in valid_headers):
        code = "graph TD\n" + stripped
        fixes.append("added_missing_mermaid_header")
    # ->|text| → -->|text|
    fixed = re.sub(r"->(\|[^|]+\|)", r"-->\1", code)
    if fixed != code:
        fixes.append("fixed_mermaid_arrow_syntax")
        code = fixed
    return code, fixes


def check_mathjax_balance(text: str) -> List[str]:
    """Return error messages if MathJax delimiters are unbalanced."""
    errors: List[str] = []
    if text.count("\\[") != text.count("\\]"):
        errors.append(f"unbalanced_block_mathjax (opens={text.count(chr(92)+'[')} closes={text.count(chr(92)+']')})")
    if text.count("\\(") != text.count("\\)"):
        errors.append(f"unbalanced_inline_mathjax (opens={text.count(chr(92)+'(')} closes={text.count(chr(92)+')')})")
    return errors


def repair_t14_visual_scene(card: dict) -> Tuple[dict, List[str]]:
    """Move T14 visual_scene from content to interactivity if wrongly placed."""
    fixes: List[str] = []
    if card.get("template") == "T14_PegNumber":
        content = card.get("content", {})
        if "visual_scene" in content:
            # Ensure interactivity dict exists
            if "interactivity" not in card or not isinstance(card.get("interactivity"), dict):
                card["interactivity"] = {}
            if not card["interactivity"].get("visual_scene"):
                card["interactivity"]["visual_scene"] = content["visual_scene"]
            # Keep it in content too since REQUIRED_FIELDS for T14 lists it there
            # (validator checks content["visual_scene"]) — leave in place
    return card, fixes


# ---------------------------------------------------------------------------
# Core per-card auditor
# ---------------------------------------------------------------------------

def audit_card(card: dict, file_pillar: Optional[str], seen_ids: set) -> Tuple[dict, List[str], List[str]]:
    """
    Returns (fixed_card, fixes_applied, unfixable_issues).
    Mutates `seen_ids` to track duplicate IDs.
    """
    fixes: List[str] = []
    issues: List[str] = []

    # -- Ensure basic structure --
    if not isinstance(card, dict):
        return card, [], ["card_not_a_dict"]

    # -- ID deduplication --
    card_id = card.get("id", "")
    if card_id in seen_ids:
        new_id = card_id + "_" + uuid.uuid4().hex[:6]
        card["id"] = new_id
        fixes.append(f"deduplicated_id: '{card_id}' → '{new_id}'")
    else:
        seen_ids.add(card_id)

    # -- Template validation --
    template = card.get("template", "")
    if template not in VALID_TEMPLATES:
        issues.append(f"unknown_template: '{template}'")
        return card, fixes, issues  # can't validate further without known template

    # -- Metadata: missing 'pillar' field --
    metadata = card.get("metadata", {})
    if not isinstance(metadata, dict):
        card["metadata"] = {}
        metadata = card["metadata"]
        fixes.append("replaced_invalid_metadata_with_empty_dict")

    if not metadata.get("pillar", "").strip():
        if file_pillar:
            metadata["pillar"] = file_pillar
            fixes.append(f"added_missing_pillar: '{file_pillar}'")
        else:
            issues.append("missing_pillar_in_metadata")

    # -- Content checks --
    content = card.get("content", {})
    if not isinstance(content, dict):
        issues.append("content_is_not_a_dict")
        return card, fixes, issues

    # Repair Cloze in text / gap_text / prompt
    for field in ["text", "gap_text", "prompt"]:
        if field in content and isinstance(content[field], str):
            repaired, cloze_fixes = repair_cloze(content[field])
            if cloze_fixes:
                content[field] = repaired
                fixes.extend(cloze_fixes)

    # Repair Mermaid code
    if "mermaid_code" in content and isinstance(content.get("mermaid_code"), str):
        repaired, m_fixes = repair_mermaid(content["mermaid_code"])
        if m_fixes:
            content["mermaid_code"] = repaired
            fixes.extend(m_fixes)

    # Repair Mermaid embedded in explanation
    if "explanation" in content and isinstance(content.get("explanation"), str):
        expl = content["explanation"]
        if 'class="mermaid"' in expl:
            def _repair_div(match):
                sanitized, _ = repair_mermaid(match.group(1))
                return f'<div class="mermaid">\n{sanitized}\n</div>'
            new_expl = re.sub(r'<div class="mermaid">\s*(.*?)\s*</div>', _repair_div, expl, flags=re.DOTALL)
            if new_expl != expl:
                content["explanation"] = new_expl
                fixes.append("repaired_mermaid_in_explanation_div")

    # T14: move visual_scene to interactivity if missing there
    card, t14_fixes = repair_t14_visual_scene(card)
    fixes.extend(t14_fixes)

    # MathJax balance check (whole card as JSON string)
    card_str = json.dumps(card, ensure_ascii=False)
    math_errors = check_mathjax_balance(card_str)
    issues.extend(math_errors)

    # Required field checks
    req = REQUIRED_FIELDS.get(template, [])
    for field in req:
        val = content.get(field)
        if val is None or (isinstance(val, str) and not val.strip()):
            issues.append(f"missing_required_field: content.{field}")

    # Short explanation check (< 20 chars, non-empty)
    expl_val = content.get("explanation", "")
    if isinstance(expl_val, str) and 0 < len(expl_val.strip()) < 20:
        issues.append(f"explanation_too_short ({len(expl_val.strip())} chars)")

    # Spanish field empty check for templates that require it
    spanish_templates = {"T1_Cloze", "T2_DualCoding", "T4_Scenario", "T7_Pronunciation",
                         "T12_SpeakingPractice", "T13_MnemonicPalace"}
    if template in spanish_templates:
        sp = content.get("spanish", "")
        if isinstance(sp, str) and not sp.strip():
            issues.append("missing_spanish_translation")

    return card, fixes, issues


# ---------------------------------------------------------------------------
# Per-file processor
# ---------------------------------------------------------------------------

def process_file(json_path: Path) -> Dict[str, Any]:
    """Load, audit, fix, and overwrite a single JSON deck file."""
    rel_path = str(json_path.relative_to(DECKS_ROOT.parent))
    pillar = infer_pillar(json_path)

    try:
        raw = json_path.read_text(encoding="utf-8")
        cards: List[dict] = json.loads(raw)
    except json.JSONDecodeError as e:
        return {
            "file": rel_path,
            "pillar": pillar,
            "cards_total": 0,
            "cards_fixed": 0,
            "cards_with_issues": 0,
            "fixes": [],
            "issues": [],
            "file_error": f"JSON parse error: {e}",
        }
    except Exception as e:
        return {
            "file": rel_path,
            "pillar": pillar,
            "cards_total": 0,
            "cards_fixed": 0,
            "cards_with_issues": 0,
            "fixes": [],
            "issues": [],
            "file_error": str(e),
        }

    if not isinstance(cards, list):
        return {
            "file": rel_path,
            "pillar": pillar,
            "cards_total": 0,
            "cards_fixed": 0,
            "cards_with_issues": 0,
            "fixes": [],
            "issues": [],
            "file_error": "Root element is not a JSON array",
        }

    seen_ids: set = set()
    file_fixes: List[Dict] = []
    file_issues: List[Dict] = []
    fixed_cards: List[dict] = []
    cards_fixed_count = 0
    cards_with_issues_count = 0

    for i, card in enumerate(cards):
        fixed_card, fixes, issues = audit_card(card, pillar, seen_ids)
        fixed_cards.append(fixed_card)

        card_id = fixed_card.get("id", f"index_{i}")
        template = fixed_card.get("template", "UNKNOWN")

        if fixes:
            cards_fixed_count += 1
            file_fixes.append({"card_id": card_id, "template": template, "fixes": fixes})

        if issues:
            cards_with_issues_count += 1
            file_issues.append({"card_id": card_id, "template": template, "issues": issues})

    # Write fixed file back (preserve structure)
    has_any_fixes = cards_fixed_count > 0
    if has_any_fixes:
        fixed_json = json.dumps(fixed_cards, indent=2, ensure_ascii=False)
        json_path.write_text(fixed_json, encoding="utf-8")

    return {
        "file": rel_path,
        "pillar": pillar,
        "cards_total": len(cards),
        "cards_fixed": cards_fixed_count,
        "cards_with_issues": cards_with_issues_count,
        "was_written": has_any_fixes,
        "fixes": file_fixes,
        "issues": file_issues,
        "file_error": None,
    }


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run_audit() -> None:
    # Ensure UTF-8 output on Windows terminals
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print("=" * 70)
    print("  Anki ADK -- Full Data Quality Audit & Auto-Fix")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    json_files = sorted(DECKS_ROOT.rglob("*.json"))
    print(f"\n[DIR] Found {len(json_files)} JSON deck files under {DECKS_ROOT}\n")

    all_results: List[Dict] = []
    total_cards = 0
    total_fixed = 0
    total_issues = 0
    total_file_errors = 0
    files_rewritten = 0

    template_distribution: Dict[str, int] = defaultdict(int)
    issue_types: Dict[str, int] = defaultdict(int)

    for json_path in json_files:
        result = process_file(json_path)
        all_results.append(result)

        total_cards += result["cards_total"]
        total_fixed += result["cards_fixed"]
        total_issues += result["cards_with_issues"]
        if result.get("file_error"):
            total_file_errors += 1
        if result.get("was_written"):
            files_rewritten += 1

        # Aggregate template distribution from the (now fixed) file
        if not result.get("file_error"):
            try:
                cards = json.loads((DECKS_ROOT.parent / result["file"]).read_text(encoding="utf-8"))
                for card in cards:
                    tpl = card.get("template", "UNKNOWN")
                    template_distribution[tpl] += 1
            except Exception:
                pass

        # Aggregate issue type counts
        for issue_record in result.get("issues", []):
            for iss in issue_record.get("issues", []):
                # Normalize to category
                key = iss.split(":")[0].split("(")[0].strip()
                issue_types[key] += 1

        # Console progress
        status_icon = "[OK]" if not result.get("file_error") else "[ERR]"
        fixed_icon = f"  [{result['cards_fixed']} fixed, {result['cards_with_issues']} flagged]" if result["cards_total"] else ""
        print(f"  {status_icon} {result['file']} ({result['cards_total']} cards){fixed_icon}")

    # -----------------------------------------------------------------------
    # Summary object
    # -----------------------------------------------------------------------
    summary = {
        "generated_at": datetime.now().isoformat(),
        "totals": {
            "files_scanned": len(json_files),
            "files_with_parse_errors": total_file_errors,
            "files_rewritten": files_rewritten,
            "cards_total": total_cards,
            "cards_auto_fixed": total_fixed,
            "cards_with_remaining_issues": total_issues,
            "cards_clean": total_cards - total_issues,
        },
        "template_distribution": dict(sorted(template_distribution.items())),
        "issue_type_counts": dict(sorted(issue_types.items(), key=lambda x: -x[1])),
        "per_file_results": all_results,
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    # -----------------------------------------------------------------------
    # Markdown report
    # -----------------------------------------------------------------------
    md_lines: List[str] = []
    md_lines.append("# Anki ADK — Data Quality Audit Report")
    md_lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    md_lines.append("## Summary")
    md_lines.append(f"| Metric | Value |")
    md_lines.append(f"|--------|-------|")
    md_lines.append(f"| Files scanned | {len(json_files)} |")
    md_lines.append(f"| Files rewritten (auto-fixed) | {files_rewritten} |")
    md_lines.append(f"| Files with parse errors | {total_file_errors} |")
    md_lines.append(f"| Total cards | {total_cards} |")
    md_lines.append(f"| Cards auto-fixed | {total_fixed} |")
    md_lines.append(f"| Cards with remaining issues | {total_issues} |")
    md_lines.append(f"| Clean cards | {total_cards - total_issues} |")
    md_lines.append(f"| Data quality score | {round((total_cards - total_issues) / max(total_cards, 1) * 100, 1)}% |")

    md_lines.append("\n## Template Distribution")
    md_lines.append("| Template | Cards |")
    md_lines.append("|----------|-------|")
    for tpl, count in sorted(template_distribution.items(), key=lambda x: -x[1]):
        md_lines.append(f"| {tpl} | {count} |")

    md_lines.append("\n## Issue Type Breakdown")
    md_lines.append("| Issue | Occurrences |")
    md_lines.append("|-------|-------------|")
    for iss, count in sorted(issue_types.items(), key=lambda x: -x[1]):
        md_lines.append(f"| {iss} | {count} |")

    md_lines.append("\n## Files With Remaining Issues")
    md_lines.append("| File | Cards | Fixed | Flagged |")
    md_lines.append("|------|-------|-------|---------|")
    for r in sorted(all_results, key=lambda x: -x["cards_with_issues"]):
        if r["cards_with_issues"] > 0 or r.get("file_error"):
            err_note = f" ⚠️ {r['file_error']}" if r.get("file_error") else ""
            md_lines.append(f"| {r['file']}{err_note} | {r['cards_total']} | {r['cards_fixed']} | {r['cards_with_issues']} |")

    md_lines.append("\n## Detailed Issues Per File\n")
    for r in all_results:
        if r.get("issues"):
            md_lines.append(f"### `{r['file']}`")
            for rec in r["issues"]:
                issues_str = "; ".join(rec["issues"])
                md_lines.append(f"- **[{rec['card_id']}]** `{rec['template']}` → {issues_str}")
            md_lines.append("")

    MD_REPORT_PATH.write_text("\n".join(md_lines), encoding="utf-8")

    # -----------------------------------------------------------------------
    # Final console summary
    # -----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("  AUDIT COMPLETE")
    print("=" * 70)
    print(f"  [STAT] Files scanned        : {len(json_files)}")
    print(f"  [WRITE] Files rewritten     : {files_rewritten}")
    print(f"  [CARDS] Cards total         : {total_cards}")
    print(f"  [FIXED] Cards auto-fixed    : {total_fixed}")
    print(f"  [WARN]  Cards flagged       : {total_issues}")
    clean_pct = round((total_cards - total_issues) / max(total_cards, 1) * 100, 1)
    print(f"  [SCORE] Quality score       : {clean_pct}%")
    print(f"\n  [REPORT] JSON -> {REPORT_PATH}")
    print(f"  [REPORT] MD   -> {MD_REPORT_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    run_audit()
