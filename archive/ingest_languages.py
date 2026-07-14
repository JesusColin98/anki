import os
import re
import json

root_dir = r"G:\My Drive\ocularis\languages"
database_file = "anki_cards_database.json"

lang_map = {
    "DE": "German",
    "FR": "French",
    "ES": "Spanish",
    "EN": "English",
    "IT": "Italian",
    "PT": "Portuguese",
    "RU": "Russian",
    "ZH": "Chinese",
    "JA": "Japanese",
    "KO": "Korean"
}

def parse_frontmatter(content):
    meta = {}
    fm_match = re.search(r"^---([\s\S]*?)---", content)
    if fm_match:
        fm_text = fm_match.group(1)
        for line in fm_text.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip().strip("'\"")
    return meta

def extract_flashcards_from_curriculum(content, meta, file_path):
    cards = []
    lines = content.splitlines()
    in_flashcards = False
    
    lang_code = meta.get("language")
    if not lang_code:
        base = os.path.basename(file_path)
        prefix = base.split("_")[0]
        if prefix in lang_map:
            lang_code = prefix
            
    lang_name = lang_map.get(lang_code, "UnknownLanguage")
    level = meta.get("level", "A1")
    topic = meta.get("topic", "General Vocabulary")
    
    clean_topic = topic.replace(" ", "_").replace("&", "and")
    deck_name = f"{lang_name}::{level}_Beginner::{clean_topic}" if "A1" in level or "A2" in level else f"{lang_name}::{level}_Intermediate::{clean_topic}"
    if "C1" in level or "C2" in level:
        deck_name = f"{lang_name}::{level}_Advanced::{clean_topic}"
        
    for line in lines:
        if "### Flashcards" in line or "## Flashcards" in line:
            in_flashcards = True
            continue
        if in_flashcards:
            if line.startswith("#") and not line.startswith("### Flashcards") and not line.startswith("## Flashcards"):
                break
                
            match = re.match(r"^\s*\*\*(.*?)\*\*\s*[—\-–]\s*(.*)$", line)
            if match:
                term = match.group(1).strip()
                definition = match.group(2).strip()
                
                definition_clean = re.sub(r"\s*\([a-zA-Z\s]+\)\.?$", "", definition).strip()
                definition_clean = definition_clean.rstrip(".")
                
                text = f"In {lang_name}, how do you say '{definition_clean}'? {{{{c1::{term}}}}}"
                explanation = f"Vocabulary for the topic '{topic}'. Level: {level}."
                spanish_trans = f"¿Cómo se dice '{definition_clean}' en {lang_name}? {term}"
                
                card = {
                    "deck": deck_name,
                    "scenario": f"{lang_name} {level}: {topic} 🗣️",
                    "text": text,
                    "explanation": explanation,
                    "usage": f"Term: <code>{term}</code> | Meaning: {definition_clean}",
                    "spanish": spanish_trans,
                    "tags": ["languages_path", lang_name.lower(), level.lower(), clean_topic.lower()]
                }
                cards.append(card)
    return cards

def extract_phonetics(content, file_path):
    cards = []
    base = os.path.basename(file_path)
    lang_name = base.replace(".md", "").strip()
    if lang_name == "Mandarin Chinese":
        lang_name = "Chinese"
        
    deck_name = f"{lang_name}::Phonetics"
    
    # 1. Parse Pronunciation Rules
    rules = re.findall(r"^\s*(?:\d+\.|\*|\-)\s*\*\*(.*?)\*\*\s*[:—\-–]\s*(.*)$", content, re.MULTILINE)
    for rule_name, rule_desc in rules:
        rule_name = rule_name.strip()
        rule_desc = rule_desc.strip()
        
        text = f"In {lang_name} phonetics, the rule of {{{{c1::{rule_name}}}}} is defined as: {rule_desc}"
        explanation = f"Phonetics and pronunciation guide for {lang_name}."
        spanish_trans = f"En la fonética de {lang_name}, la regla de '{rule_name}' es: {rule_desc}"
        
        card = {
            "deck": deck_name,
            "scenario": f"{lang_name} Phonetics 🗣️",
            "text": text,
            "explanation": explanation,
            "usage": f"Rule: <code>{rule_name}</code><br>Description: {rule_desc}",
            "spanish": spanish_trans,
            "tags": ["languages_path", lang_name.lower(), "phonetics"]
        }
        cards.append(card)
        
    # 2. Parse Tip Blocks line-by-line (Safe from backtracking)
    lines = content.splitlines()
    in_tip = False
    tip_title = ""
    tip_lines = []
    
    for line in lines:
        line_strip = line.strip()
        tip_start = re.match(r"^>\s*\[!(tip|info)\]\s*(.*)$", line_strip, re.IGNORECASE)
        if tip_start:
            if in_tip and tip_title and tip_lines:
                content_str = " ".join(tip_lines)
                text = f"What is the {lang_name} pronunciation shortcut/tip for {{{{c1::{tip_title}}}}}? {content_str}"
                explanation = f"Pronunciation tip/shortcut for {lang_name}."
                spanish_trans = f"¿Cuál es el atajo/consejo de pronunciación de {lang_name} para '{tip_title}'? {content_str}"
                cards.append({
                    "deck": deck_name,
                    "scenario": f"{lang_name} Phonetics Tips 💡",
                    "text": text,
                    "explanation": explanation,
                    "usage": f"Tip: <code>{tip_title}</code><br>{content_str}",
                    "spanish": spanish_trans,
                    "tags": ["languages_path", lang_name.lower(), "phonetics", "tips"]
                })
            
            in_tip = True
            tip_title = tip_start.group(2).strip()
            if not tip_title:
                tip_title = "General Tip"
            tip_lines = []
            continue
            
        if in_tip:
            if line_strip.startswith(">"):
                content_line = line_strip.lstrip(">").strip()
                if content_line:
                    tip_lines.append(content_line)
            else:
                if tip_title and tip_lines:
                    content_str = " ".join(tip_lines)
                    text = f"What is the {lang_name} pronunciation shortcut/tip for {{{{c1::{tip_title}}}}}? {content_str}"
                    explanation = f"Pronunciation tip/shortcut for {lang_name}."
                    spanish_trans = f"¿Cuál es el atajo/consejo de pronunciación de {lang_name} para '{tip_title}'? {content_str}"
                    cards.append({
                        "deck": deck_name,
                        "scenario": f"{lang_name} Phonetics Tips 💡",
                        "text": text,
                        "explanation": explanation,
                        "usage": f"Tip: <code>{tip_title}</code><br>{content_str}",
                        "spanish": spanish_trans,
                        "tags": ["languages_path", lang_name.lower(), "phonetics", "tips"]
                    })
                in_tip = False
                tip_title = ""
                tip_lines = []
                
    if in_tip and tip_title and tip_lines:
        content_str = " ".join(tip_lines)
        text = f"What is the {lang_name} pronunciation shortcut/tip for {{{{c1::{tip_title}}}}}? {content_str}"
        explanation = f"Pronunciation tip/shortcut for {lang_name}."
        spanish_trans = f"¿Cuál es el atajo/consejo de pronunciación de {lang_name} para '{tip_title}'? {content_str}"
        cards.append({
            "deck": deck_name,
            "scenario": f"{lang_name} Phonetics Tips 💡",
            "text": text,
            "explanation": explanation,
            "usage": f"Tip: <code>{tip_title}</code><br>{content_str}",
            "spanish": spanish_trans,
            "tags": ["languages_path", lang_name.lower(), "phonetics", "tips"]
        })
        
    return cards

def run_ingestion():
    if os.path.exists(database_file):
        with open(database_file, "r", encoding="utf-8") as f:
            database = json.load(f)
    else:
        database = []
        
    existing_texts = set(c['text'] for c in database)
    
    parsed_count = 0
    phonetics_count = 0
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                
                if "Dashboard" in file or file.startswith("_"):
                    continue
                    
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                meta = parse_frontmatter(content)
                
                if "Phonetics" in root_dir or "Phonetics" in root:
                    cards = extract_phonetics(content, file_path)
                    for c in cards:
                        if c['text'] not in existing_texts:
                            database.append(c)
                            existing_texts.add(c['text'])
                            phonetics_count += 1
                else:
                    cards = extract_flashcards_from_curriculum(content, meta, file_path)
                    for c in cards:
                        if c['text'] not in existing_texts:
                            database.append(c)
                            existing_texts.add(c['text'])
                            parsed_count += 1
                            
    with open(database_file, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
        
    print(f"\nIngestion Completed:")
    print(f" - Added {parsed_count} curriculum language cards.")
    print(f" - Added {phonetics_count} phonetics rules/tips cards.")
    print(f" - Total cards in database now: {len(database)}")

if __name__ == "__main__":
    run_ingestion()
