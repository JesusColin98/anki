#!/usr/bin/env python3
"""
deep_content_audit.py — Deep Content Quality Analyzer
======================================================
Goes beyond syntax — inspects SEMANTIC quality issues:

1. Template mismatch: T1_Cloze used for scenario cards (should be T4_Scenario)
2. Spanish field contains the English word instead of full translation
   e.g. "Estoy buscando milk." → should be "Estoy buscando leche."
3. Boilerplate/generic explanations (copy-paste LLM artifacts)
4. 'usage' field is boilerplate (same across hundreds of cards)
5. 'explanation' repeats the cloze word literally instead of explaining it
6. Duplicate texts within a file (same sentence, different IDs)
7. Cloze only covers a single trivial word (no real learning value)
8. Missing T4_Scenario template when card has 'scenario', 'target_phrase', 'usage', 'spanish'
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DECKS_ROOT = Path(__file__).parent / "decks"
REPORT_PATH = Path(__file__).parent / "scratch" / "deep_audit_report.json"
MD_PATH = Path(__file__).parent / "scratch" / "deep_audit_report.md"

# Known boilerplate patterns (regex) in explanation
BOILERPLATE_EXPLANATION_PATTERNS = [
    r"^This is a practical phrase used in .+ to sound natural and useful in real conversations\.$",
    r"^This (phrase|expression|term) is (commonly|frequently|often|widely) used",
    r"^A practical phrase for",
    r"^Useful (phrase|expression) (for|in|when)",
]

# Known boilerplate patterns in usage field
BOILERPLATE_USAGE_PATTERNS = [
    r"^Useful for practicing realistic English in .+\.$",
    r"^Practice this phrase in",
    r"^Use this (in|when|for)",
]

BOILERPLATE_EXPL_RE = [re.compile(p, re.IGNORECASE) for p in BOILERPLATE_EXPLANATION_PATTERNS]
BOILERPLATE_USAGE_RE = [re.compile(p, re.IGNORECASE) for p in BOILERPLATE_USAGE_PATTERNS]


def has_boilerplate_explanation(text: str) -> bool:
    return any(r.match(text.strip()) for r in BOILERPLATE_EXPL_RE)


def has_boilerplate_usage(text: str) -> bool:
    return any(r.match(text.strip()) for r in BOILERPLATE_USAGE_RE)


def spanish_contains_raw_english_word(text_field: str, spanish_field: str) -> bool:
    """Check if spanish field literally embeds the cloze word in English."""
    # Extract cloze words from text
    cloze_words = re.findall(r'\{\{c\d+::([^}]+)\}\}', text_field)
    for word in cloze_words:
        word_clean = word.strip().lower()
        if len(word_clean) < 3:
            continue  # Too short to be meaningful
        # Check if that exact English word appears in the Spanish translation
        if re.search(r'\b' + re.escape(word_clean) + r'\b', spanish_field.lower()):
            return True, word_clean
    return False, None


def is_trivial_cloze(text: str) -> bool:
    """Cloze covers a single common/trivial word with no pedagogical depth."""
    cloze_words = re.findall(r'\{\{c\d+::([^}]+)\}\}', text)
    trivial = {"the", "a", "an", "is", "are", "was", "were", "it", "this", "that",
               "and", "or", "but", "in", "on", "at", "to", "of", "for", "with"}
    for word in cloze_words:
        if word.strip().lower() in trivial:
            return True
    return False


def should_be_t4(card: dict) -> bool:
    """T1_Cloze cards that have scenario+target_phrase+usage+spanish should be T4_Scenario."""
    if card.get("template") != "T1_Cloze":
        return False
    content = card.get("content", {})
    # If they have 'target_phrase' explicitly it's a mismatch
    return "target_phrase" in content


def audit_file_deep(json_path: Path) -> dict:
    rel = str(json_path.relative_to(DECKS_ROOT.parent))
    try:
        cards = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"file": rel, "error": str(e), "issues": []}
    if not isinstance(cards, list):
        return {"file": rel, "error": "not a list", "issues": []}

    issues = []
    seen_texts = Counter()

    # First pass: collect all texts for duplicate detection
    for card in cards:
        content = card.get("content", {})
        text = content.get("text", content.get("prompt", "")).strip()
        if text:
            seen_texts[text] += 1

    # Second pass: per-card analysis
    for card in cards:
        card_id = card.get("id", "?")
        template = card.get("template", "?")
        content = card.get("content", {})
        card_issues = []

        text = content.get("text", content.get("prompt", "")).strip()
        explanation = content.get("explanation", "").strip()
        usage = content.get("usage", "").strip()
        spanish = content.get("spanish", "").strip()

        # 1. Boilerplate explanation
        if explanation and has_boilerplate_explanation(explanation):
            card_issues.append({
                "type": "boilerplate_explanation",
                "detail": explanation[:100]
            })

        # 2. Boilerplate usage
        if usage and has_boilerplate_usage(usage):
            card_issues.append({
                "type": "boilerplate_usage",
                "detail": usage[:100]
            })

        # 3. Spanish contains raw English cloze word
        if text and spanish:
            has_raw, word = spanish_contains_raw_english_word(text, spanish)
            if has_raw:
                card_issues.append({
                    "type": "spanish_has_english_word",
                    "detail": f"cloze='{word}' found literally in spanish='{spanish[:80]}'"
                })

        # 4. Trivial cloze
        if text and is_trivial_cloze(text):
            card_issues.append({
                "type": "trivial_cloze",
                "detail": text[:100]
            })

        # 5. Duplicate text in same file
        if text and seen_texts[text] > 1:
            card_issues.append({
                "type": "duplicate_text_in_file",
                "detail": f"appears {seen_texts[text]}x: '{text[:80]}'"
            })

        # 6. Template mismatch: should be T4
        if should_be_t4(card):
            card_issues.append({
                "type": "wrong_template_should_be_t4",
                "detail": "Has target_phrase field but uses T1_Cloze"
            })

        # 7. Explanation literally repeats the cloze answer
        if text and explanation:
            cloze_words = re.findall(r'\{\{c\d+::([^}]+)\}\}', text)
            for cw in cloze_words:
                cw_clean = cw.strip().lower()
                if len(cw_clean) > 3 and explanation.lower().startswith(cw_clean):
                    card_issues.append({
                        "type": "explanation_echoes_cloze",
                        "detail": f"explanation starts with cloze answer '{cw_clean}'"
                    })

        if card_issues:
            issues.append({
                "card_id": card_id,
                "template": template,
                "issues": card_issues
            })

    # Aggregate counts
    type_counts = Counter()
    for rec in issues:
        for iss in rec["issues"]:
            type_counts[iss["type"]] += 1

    return {
        "file": rel,
        "cards_total": len(cards),
        "cards_with_issues": len(issues),
        "issue_type_counts": dict(type_counts),
        "issues": issues,
        "error": None,
    }


def run() -> None:
    json_files = sorted(DECKS_ROOT.rglob("*.json"))
    # Exclude non-card JSONs
    exclude = {"index.json", "manifest.json"}
    json_files = [f for f in json_files if f.name not in exclude]

    print(f"Deep auditing {len(json_files)} deck files...")

    all_results = []
    grand_type_counts = Counter()
    total_cards = 0
    total_issues = 0

    for f in json_files:
        r = audit_file_deep(f)
        all_results.append(r)
        total_cards += r.get("cards_total", 0)
        total_issues += r.get("cards_with_issues", 0)
        for k, v in r.get("issue_type_counts", {}).items():
            grand_type_counts[k] += v
        if r.get("cards_with_issues", 0):
            print(f"  [ISSUES] {r['file']} — {r['cards_with_issues']} cards flagged")

    print(f"\nTotal cards: {total_cards}")
    print(f"Cards with content issues: {total_issues}")
    print("\nIssue type breakdown:")
    for k, v in grand_type_counts.most_common():
        print(f"  {k}: {v}")

    summary = {
        "total_cards": total_cards,
        "cards_with_issues": total_issues,
        "issue_type_counts": dict(grand_type_counts),
        "per_file": all_results,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    # Markdown
    lines = []
    lines.append("# Deep Content Quality Audit")
    lines.append(f"\n**Total cards:** {total_cards}  **Cards flagged:** {total_issues}\n")
    lines.append("## Issue Type Summary")
    lines.append("| Issue | Cards affected |")
    lines.append("|-------|----------------|")
    for k, v in grand_type_counts.most_common():
        lines.append(f"| {k} | {v} |")
    lines.append("\n## Per-File Breakdown (files with issues only)")
    lines.append("| File | Total | Flagged | Top issue |")
    lines.append("|------|-------|---------|-----------|")
    for r in sorted(all_results, key=lambda x: -x.get("cards_with_issues", 0)):
        if r.get("cards_with_issues", 0):
            top = max(r["issue_type_counts"], key=r["issue_type_counts"].get, default="-")
            lines.append(f"| {r['file']} | {r['cards_total']} | {r['cards_with_issues']} | {top} |")
    lines.append("\n## Sample Issue Details (first 20 per file with issues)")
    for r in all_results:
        if r.get("issues"):
            lines.append(f"\n### `{r['file']}`")
            for rec in r["issues"][:20]:
                for iss in rec["issues"]:
                    lines.append(f"- **[{rec['card_id']}]** `{iss['type']}` → {iss['detail']}")
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReports saved:\n  {REPORT_PATH}\n  {MD_PATH}")


if __name__ == "__main__":
    run()
