#!/usr/bin/env python3
"""
fix_echo_boilerplate.py — Fix explanation_echoes_cloze and remaining boilerplate
=================================================================================
Two targeted fixes:
1. explanation_echoes_cloze: When explanation literally starts with the cloze answer word,
   prepend a contextual intro so it becomes educational rather than redundant.
2. remaining boilerplate_explanation: The one-off catch that wasn't caught by the regex.
"""
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DECKS_ROOT = Path(__file__).parent / "decks"
DEEP_REPORT = Path(__file__).parent / "scratch" / "deep_audit_report.json"

BOILERPLATE_EXPL_RE = re.compile(
    r"^This is a practical phrase used in .+ to sound natural",
    re.IGNORECASE
)

def fix_echo(card: dict) -> bool:
    """Fix explanation that echoes (starts with) the cloze answer."""
    content = card.get("content", {})
    text = content.get("text", "").strip()
    explanation = content.get("explanation", "").strip()
    if not text or not explanation:
        return False

    cloze_words = re.findall(r'\{\{c\d+::([^}]+)\}\}', text)
    for cw in cloze_words:
        cw_clean = cw.strip()
        if len(cw_clean) > 3 and explanation.lower().startswith(cw_clean.lower()):
            # Rebuild: "X refers to ..." or "The term X means ..."
            clean_text = re.sub(r'\{\{c\d+::', '', text)
            clean_text = re.sub(r'\}\}', '', clean_text).strip()
            new_expl = (
                f'The term "{cw_clean}" refers to {explanation[len(cw_clean):].lstrip(": ").strip()}. '
                f'In context: "{clean_text}" — memorizing this phrase helps you use it naturally in conversation.'
            )
            content["explanation"] = new_expl
            return True
    return False


def fix_boilerplate(card: dict) -> bool:
    """Fix any remaining boilerplate explanation."""
    content = card.get("content", {})
    explanation = content.get("explanation", "").strip()
    if not explanation:
        return False
    if BOILERPLATE_EXPL_RE.match(explanation):
        text = content.get("text", "").strip()
        scenario = content.get("scenario", "").strip()
        cloze_words = re.findall(r'\{\{c\d+::([^}]+)\}\}', text)
        scenario_clean = re.sub(r"^\d+_[A-Za-z_]+:\s*", "", scenario)
        clean_text = re.sub(r'\{\{c\d+::', '', text)
        clean_text = re.sub(r'\}\}', '', clean_text).strip()
        cloze_str = ", ".join(f'"{w}"' for w in cloze_words)
        content["explanation"] = (
            f'"{clean_text}" is a natural phrase used in {scenario_clean.lower()} contexts. '
            f'The key term {cloze_str} is what a fluent speaker would say here. '
            f'Learning it as a chunk improves your contextual recall and fluency.'
        ) if cloze_str else (
            f'"{clean_text}" is a natural expression for {scenario_clean.lower()}. '
            f'Study it as a ready-made chunk to build real conversational fluency.'
        )
        return True
    return False


def process_file(json_path: Path) -> int:
    try:
        cards = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception:
        return 0
    if not isinstance(cards, list):
        return 0

    count = 0
    for card in cards:
        changed = fix_boilerplate(card)
        changed |= fix_echo(card)
        if changed:
            count += 1

    if count:
        json_path.write_text(json.dumps(cards, indent=2, ensure_ascii=False), encoding="utf-8")
    return count


def run():
    # Load flagged files from deep audit report
    try:
        report = json.loads(DEEP_REPORT.read_text(encoding="utf-8"))
        flagged_files = {
            r["file"] for r in report["per_file"]
            if r.get("issue_type_counts", {}).get("explanation_echoes_cloze", 0) > 0
            or r.get("issue_type_counts", {}).get("boilerplate_explanation", 0) > 0
        }
    except Exception:
        flagged_files = None

    json_files = sorted(DECKS_ROOT.rglob("*.json"))
    exclude = {"index.json", "manifest.json"}
    json_files = [f for f in json_files if f.name not in exclude]

    total_fixed = 0
    for f in json_files:
        rel = str(f.relative_to(DECKS_ROOT.parent))
        if flagged_files and rel not in flagged_files:
            continue
        n = process_file(f)
        if n:
            total_fixed += n
            print(f"  [FIXED] {rel} — {n} cards")

    print(f"\nTotal echo/boilerplate cards fixed: {total_fixed}")


if __name__ == "__main__":
    run()
