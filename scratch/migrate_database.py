#!/usr/bin/env python3
import os
import json
import hashlib
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
DECKS_DIR = BASE_DIR / "decks"

# Book mapping for tags
BOOK_TAGS = {
    "gap_selling": "source::gap_selling",
    "spin_selling": "source::spin_selling",
    "challenger_sale": "source::challenger_sale",
    "objections": "source::objections",
    "fanatical_prospecting": "source::fanatical_prospecting",
    "memory_craft": "source::memory_craft",
    "brilliant_memory": "source::brilliant_memory",
    "moonwalking": "source::moonwalking_with_einstein",
    "memory_book": "source::the_memory_book",
    "unlimited_memory": "source::unlimited_memory",
    "art_of_memory": "source::art_of_memory",
    "make_it_stick": "source::make_it_stick",
    "ultralearning": "source::ultralearning",
    "smart_notes": "source::how_to_take_smart_notes",
    "second_brain": "source::building_a_second_brain",
    "mind_for_numbers": "source::a_mind_for_numbers",
    "superlearner": "source::become_a_superlearner",
    "essentialism": "source::essentialism",
    "four_thousand_weeks": "source::four_thousand_weeks",
    "tiny_habits": "source::tiny_habits",
    "philosophy_meaning": "source::philosophy_meaning",
    "communication_influence": "source::communication_influence"
}

def detect_template(card: dict) -> str:
    if "word_pairs" in card:
        return "T8_MinimalPair"
    elif "grapheme_pattern" in card:
        return "T10_ReadingPatternDrill"
    elif "gap_text" in card and "full_transcript" in card:
        return "T9_ListeningChunk"
    elif "shadowing_script" in card:
        return "T11_ExecutivePitch"
    elif "fast_pronunciation" in card:
        return "T7_Pronunciation"
    elif "formula_latex" in card:
        return "T5_MathJax"
    elif "correct_option" in card:
        return "T6_Quiz"
    elif "mermaid_code" in card or (isinstance(card.get("explanation"), str) and "class=\"mermaid\"" in card["explanation"]):
        return "T2_DualCoding"
    elif "code_block" in card:
        return "T3_CodeSnippet"
    elif "model_audio_url" in card or "practice_url" in card or "recording_hint" in card:
        return "T12_SpeakingPractice"
    elif "target_phrase" in card:
        return "T4_Scenario"
    else:
        return "T1_Cloze"

def get_target_path(rel_path: Path) -> Path:
    parts = rel_path.parts
    pillar = parts[0]
    filename = rel_path.name
    filename_lower = filename.lower()
    
    # Pillar 1
    if pillar == "01_Cloud_and_Infrastructure":
        category = parts[1]
        if category == "Cybersecurity":
            if any(k in filename_lower for k in ["defense_evasion", "evasion"]):
                return Path("01_Cloud_and_Infrastructure/Cybersecurity/Red_Teaming/defense_evasion.json")
            elif "exploitation" in filename_lower and "post" not in filename_lower:
                return Path("01_Cloud_and_Infrastructure/Cybersecurity/Red_Teaming/exploitation.json")
            elif "post_exploitation" in filename_lower:
                return Path("01_Cloud_and_Infrastructure/Cybersecurity/Red_Teaming/post_exploitation.json")
            elif "reconnaissance" in filename_lower:
                return Path("01_Cloud_and_Infrastructure/Cybersecurity/Red_Teaming/reconnaissance_and_scanning.json")
            elif "incident_response" in filename_lower:
                return Path("01_Cloud_and_Infrastructure/Cybersecurity/Blue_Teaming/incident_response_and_operations.json")
            elif "security_operations" in filename_lower:
                return Path("01_Cloud_and_Infrastructure/Cybersecurity/Blue_Teaming/security_operations.json")
        elif category == "Networking":
            if "fundamentals" in filename_lower:
                return Path("01_Cloud_and_Infrastructure/Networking/Fundamentals/networking_fundamentals.json")
            elif "gcp" in filename_lower or "compute" in filename_lower:
                return Path("01_Cloud_and_Infrastructure/Networking/GCP_Cloud_Networking/vpc_and_compute_design.json")
            elif "protocols" in filename_lower:
                return Path("01_Cloud_and_Infrastructure/Networking/Protocols_and_Security/ports_and_tls_security.json")
        elif category == "Systems_Engineering":
            if "infrastructure" in filename_lower:
                return Path("01_Cloud_and_Infrastructure/Systems_Engineering/Infrastructure_as_Code/docker_and_kubernetes_orchestration.json")
            elif "linux" in filename_lower:
                return Path("01_Cloud_and_Infrastructure/Systems_Engineering/Administration/linux_command_line_and_kernel.json")

    # Pillar 2
    if pillar == "02_AI_and_Data_Science":
        category = parts[1]
        if category in ["05_mlops_and_llmops", "mlops_and_llmops", "05_MLOps_and_LLMOps", "MLOps_and_LLMOps"]:
            return Path("02_AI_and_Data_Science/MLOps_and_LLMOps/Operations/pipelines_and_observability.json")
        elif category in ["06_responsible_ai", "responsible_ai", "06_Responsible_AI", "Responsible_AI"]:
            return Path("02_AI_and_Data_Science/Governance_and_Strategy/Responsible_AI/safety_ethics_and_adversarial_defense.json")
        elif category in ["07_ai_product_and_strategy", "07_AI_Product_and_Strategy"]:
            return Path("02_AI_and_Data_Science/Governance_and_Strategy/Product_Strategy/ai_adoption_and_system_design.json")
        else:
            # Specific file merges for Tech_Map_2026, Books, and AI_Learning_Path
            if any(k in filename_lower for k in ["01_math_foundations", "02_feature_engineering", "03_supervised", "04_unsupervised", "05_evaluation", "06_optimization", "04_ai_engineering"]):
                return Path("02_AI_and_Data_Science/AI_Engineering/Classical_and_Deep_Learning/statistical_ml_and_neural_nets.json")
            elif any(k in filename_lower for k in ["02_llm_fundamentals", "03_advanced_llm", "02_reasoning_llms"]):
                return Path("02_AI_and_Data_Science/AI_Engineering/LLM_Foundations/llm_foundations_and_architectures.json")
            elif any(k in filename_lower for k in ["01_ai_agents_autonomy", "agent_frameworks", "overview"]):
                return Path("02_AI_and_Data_Science/AI_Engineering/Agentic_Systems/agents_architecture_and_reinforcement_learning.json")
            elif "04_agentic_dev_ides" in filename_lower:
                return Path("02_AI_and_Data_Science/AI_Engineering/Agentic_Systems/adk_framework_core.json")
            
            # AI Engineering general mappings
            if any(k in filename_lower for k in ["statistical_ml", "deep_learning", "recommendation", "causal", "ai_ml"]):
                return Path("02_AI_and_Data_Science/AI_Engineering/Classical_and_Deep_Learning/statistical_ml_and_neural_nets.json")
            elif any(k in filename_lower for k in ["llm_foundations", "systems_design", "optimization_and_inference", "training_systems", "generative_models"]):
                return Path("02_AI_and_Data_Science/AI_Engineering/LLM_Foundations/llm_foundations_and_architectures.json")
            elif any(k in filename_lower for k in ["prompt_engineering", "agent_evals"]):
                return Path("02_AI_and_Data_Science/AI_Engineering/LLM_Applications/prompt_engineering_and_evaluation.json")
            elif any(k in filename_lower for k in ["rag", "multimodal", "rag_systems"]):
                return Path("02_AI_and_Data_Science/AI_Engineering/LLM_Applications/rag_and_knowledge_retrieval.json")
            elif "fine_tuning" in filename_lower:
                return Path("02_AI_and_Data_Science/AI_Engineering/LLM_Applications/fine_tuning_and_adaptation.json")
            elif any(k in filename_lower for k in ["agents_and_tool", "game_ai", "agentic_systems"]):
                return Path("02_AI_and_Data_Science/AI_Engineering/Agentic_Systems/agents_architecture_and_reinforcement_learning.json")
            elif any(k in filename_lower for k in ["adk", "adk_framework_core"]):
                return Path("02_AI_and_Data_Science/AI_Engineering/Agentic_Systems/adk_framework_core.json")
            elif "tech_map_2026" in filename_lower:
                return Path("02_AI_and_Data_Science/AI_Engineering/LLM_Applications/tech_map_2026.json")

    # Pillar 3
    if pillar == "03_Languages":
        lang = parts[1]
        if lang == "English":
            if "phonetics" in rel_path.as_posix().lower():
                # Sequence rules under Phonetics/Connected_Speech_Patterns or filenames starting with digits
                if "connected_speech_patterns" in rel_path.as_posix().lower() or (filename_lower.startswith(("0", "1", "2")) and "_" in filename_lower):
                    return Path("03_Languages/English/Phonetics_and_Connected_Speech") / filename.lower()
                else:
                    return Path("03_Languages/English/Phonetics_and_Connected_Speech/colloquial_rhythm_and_flow.json")
            else:
                # Real scenarios
                if any(k in filename_lower or k in rel_path.as_posix().lower() for k in ["daily", "travel", "social"]):
                    return Path("03_Languages/English/Real_World_Scenarios/daily_and_social_interactions.json")
                elif any(k in filename_lower or k in rel_path.as_posix().lower() for k in ["workplace", "phone", "customer", "service"]):
                    return Path("03_Languages/English/Real_World_Scenarios/workplace_and_customer_service.json")
                elif any(k in filename_lower or k in rel_path.as_posix().lower() for k in ["interview", "career"]):
                    return Path("03_Languages/English/Real_World_Scenarios/interview_and_career_pitching.json")
                else:
                    return Path("03_Languages/English/Real_World_Scenarios/academic_and_medical_contexts.json")
        else:
            # Other languages
            if "beginner" in rel_path.as_posix().lower() or "a1" in rel_path.as_posix().lower():
                return Path(f"03_Languages/{lang}/A1_Beginner/greetings_pronouns_and_verbs.json")
            elif "phonetics" in rel_path.as_posix().lower():
                return Path(f"03_Languages/{lang}/Phonetics/grapheme_to_phoneme_drills.json")

    # Pillar 4
    if pillar == "04_Social_and_Humanities":
        category = parts[1]
        if category == "Philosophy":
            if any(k in filename_lower for k in ["classical", "eastern"]):
                return Path("04_Social_and_Humanities/Philosophy/Foundations_and_Schools/classical_greek_and_eastern.json")
            elif any(k in filename_lower for k in ["stoic", "meaning"]):
                return Path("04_Social_and_Humanities/Philosophy/Applied_Stoicism/stoic_principles_and_daily_practice.json")
            else:
                return Path("04_Social_and_Humanities/Philosophy/Foundations_and_Schools/modern_and_postmodern_movements.json")
        elif category == "Psychology":
            if "cognitive" in filename_lower:
                return Path("04_Social_and_Humanities/Psychology/Cognitive_and_Behavioral/cognitive_biases_and_mental_models.json")
            else:
                return Path("04_Social_and_Humanities/Psychology/Social_and_Conversational/conversational_dynamics_and_rapport.json")

    # Pillar 5
    if pillar == "05_Soft_Skills_and_Leadership":
        category = parts[1]
        if category in ["Leadership", "Leadership_Core"]:
            if any(k in filename_lower for k in ["delegation", "performance", "team"]):
                if "performance" in filename_lower:
                    return Path("05_Soft_Skills_and_Leadership/Leadership/Management/performance_metrics_and_accountability.json")
                else:
                    return Path("05_Soft_Skills_and_Leadership/Leadership/Management/delegation_coaching_and_feedback.json")
            else:
                return Path("05_Soft_Skills_and_Leadership/Leadership/Executive_Presence/pitching_public_speaking_and_influence.json")
        elif category in ["Social_Skills", "Service_Leadership", "Books"]:
            if any(k in filename_lower for k in ["active_listening", "negotiation"]):
                return Path("05_Soft_Skills_and_Leadership/Social_Skills/Communication/active_listening_and_negotiation.json")
            elif any(k in filename_lower for k in ["persuasion", "storytelling", "influence"]):
                return Path("05_Soft_Skills_and_Leadership/Social_Skills/Communication/storytelling_and_persuasion_foundations.json")
            else:
                return Path("05_Soft_Skills_and_Leadership/Social_Skills/Customer_Excellence/incident_recovery_and_crisis_handling.json")

    # Pillar 6
    if pillar == "06_Business_and_Productivity":
        category = parts[1]
        if category == "Business":
            if "sales" in rel_path.as_posix().lower() or any(k in filename_lower for k in ["selling", "prospecting", "objections"]):
                return Path("06_Business_and_Productivity/Business_and_Sales/Sales/sales_methodologies_and_objections.json")
            else:
                return Path("06_Business_and_Productivity/Business_and_Sales/Strategy/corporate_strategy_and_market_positioning.json")
        elif category == "Learning_Methods":
            return Path("06_Business_and_Productivity/Learning_and_Memory/Methodology/memory_techniques_and_systems.json")
        elif category == "Productivity":
            learning_books = ["stick", "ultra", "notes", "brain", "numbers", "superlearner"]
            if any(k in filename_lower for k in learning_books):
                return Path("06_Business_and_Productivity/Learning_and_Memory/Methodology/learning_methodology.json")
            else:
                return Path("06_Business_and_Productivity/Productivity_and_Habits/Methodology/productivity_and_habits.json")

    # Fallback default
    new_name = filename_lower.replace(" ", "_")
    return Path(pillar) / parts[1] / new_name

def migrate():
    print("=== STARTING DATABASE MIGRATION ===")
    
    # 1. Scan and parse existing cards
    all_json_files = []
    for root, dirs, files in os.walk(DECKS_DIR):
        for f in files:
            if f.endswith('.json') and f not in ['index.json', 'manifest.json']:
                all_json_files.append(Path(root) / f)

    print(f"Found {len(all_json_files)} source files.")
    
    # Group target cards by their new path
    migrated_decks = {} # Target Path -> List of nested cards

    for sf in all_json_files:
        rel_path = sf.relative_to(DECKS_DIR)
        target_rel = get_target_path(rel_path)
        target_abs = DECKS_DIR / target_rel
        
        # Determine tags based on original filename (e.g. book summaries)
        source_tags = []
        for kw, tag in BOOK_TAGS.items():
            if kw in sf.name.lower():
                source_tags.append(tag)
        
        with open(sf, "r", encoding="utf-8") as f:
            try:
                cards = json.load(f)
            except Exception as e:
                print(f"[-] Error reading {sf}: {e}")
                continue
        
        if not isinstance(cards, list):
            cards = [cards]

        print(f"Migrating: {rel_path} -> {target_rel} ({len(cards)} cards)")
        
        # Calculate 4-level deck name to preserve structural validation
        parts = target_rel.parts
        p_pillar = parts[0]
        p_cat = parts[1] # Cybersecurity
        p_sub = parts[2] # Red_Teaming
        p_deck = target_rel.stem.replace("_", " ").title().replace(" ", "_")
        target_anki_deck = f"{p_pillar}::{p_cat}::{p_sub}::{p_deck}"
        
        if target_rel not in migrated_decks:
            migrated_decks[target_rel] = []

        for card in cards:
            template = detect_template(card)
            
            # Unify tags
            tags = card.get("tags", [])
            for t in source_tags:
                if t not in tags:
                    tags.append(t)
            
            # Determine text for hashing
            text_key = card.get("text", card.get("prompt", ""))
            if not text_key:
                text_key = str(card)
            
            # Deterministic SHA256 ID
            card_id = hashlib.sha256(text_key.encode('utf-8')).hexdigest()[:16]
            
            # Auto-extract for T2_DualCoding if missing concept or mermaid_code
            extracted_fields = {}
            if template == "T2_DualCoding":
                raw_text = card.get("text", "")
                cloze_match = re.search(r"\{\{c\d+::(.*?)\}\}", raw_text)
                extracted_concept = cloze_match.group(1) if cloze_match else card.get("scenario", "General")
                if not cloze_match:
                    extracted_concept = re.sub(r"^.*?:\s*", "", extracted_concept)
                    extracted_concept = re.sub(r"[\u2600-\u27BF].*?", "", extracted_concept).strip()
                extracted_fields["concept"] = card.get("concept", extracted_concept)
                
                raw_explanation = card.get("explanation", "")
                mermaid_match = re.search(r'<div class="mermaid">\s*(.*?)\s*</div>', raw_explanation, re.DOTALL)
                if mermaid_match:
                    raw_mermaid = mermaid_match.group(1).strip()
                    # Clean explanation to remove duplicate block
                    cleaned_explanation = re.sub(r'<div class="mermaid">\s*(.*?)\s*</div>', '', raw_explanation, flags=re.DOTALL).strip()
                    card["explanation"] = cleaned_explanation
                else:
                    raw_mermaid = card.get("mermaid_code", "")
                extracted_fields["mermaid_code"] = raw_mermaid
            
            # Build nested dictionary
            nested = {
                "id": card_id,
                "deck": target_anki_deck,
                "template": template,
                "metadata": {
                    "difficulty": card.get("difficulty", "intermediate"),
                    "pillar": p_pillar,
                    "tags": tags
                },
                "content": {
                    "scenario": card.get("scenario", "General"),
                    "text": card.get("text", ""),
                    "explanation": card.get("explanation", ""),
                    "spanish": card.get("spanish", card.get("Spanish_Translation", "")),
                    "usage": card.get("usage", card.get("Usage_Examples", ""))
                },
                "mnemonics": {
                    "palace_name": card.get("palace_name", ""),
                    "locus_stop": card.get("locus_stop", ""),
                    "mnemonic_scene": card.get("mnemonic_scene", ""),
                    "peg_word": card.get("peg_word", ""),
                    "phonetic_code": card.get("phonetic_code", "")
                },
                "interactivity": {
                    "analogy": card.get("analogy", ""),
                    "interactive_mermaid": card.get("interactive_mermaid", ""),
                    "match_game_data": card.get("match_game_data", None)
                }
            }
            
            # Apply auto-extracted fields
            for k, v in extracted_fields.items():
                nested["content"][k] = v

            # Copy template-specific fields under content
            # This maintains dynamic fields so that flattening works perfectly
            for k, v in card.items():
                if k not in ["deck", "scenario", "text", "explanation", "spanish", "usage", "tags", "difficulty", "palace_name", "locus_stop", "mnemonic_scene", "peg_word", "phonetic_code", "analogy", "interactive_mermaid", "match_game_data", "concept", "mermaid_code"]:
                    nested["content"][k] = v
            
            migrated_decks[target_rel].append(nested)

    # 2. Write out migrated decks
    print("\nWriting out restructured JSON files...")
    for target_rel, nested_cards in migrated_decks.items():
        target_abs = DECKS_DIR / target_rel
        target_abs.parent.mkdir(parents=True, exist_ok=True)
        
        # If file already exists (due to merges), read and combine
        existing = []
        if target_abs.exists():
            with open(target_abs, "r", encoding="utf-8") as f:
                try:
                    existing = json.load(f)
                except Exception:
                    pass
        
        # Combine and de-duplicate by content text
        combined = existing + nested_cards
        unique = []
        seen = set()
        for c in combined:
            # Match by normalized text
            txt = c["content"].get("text", c["content"].get("prompt", "")).strip()
            if txt not in seen:
                seen.add(txt)
                unique.append(c)
        
        with open(target_abs, "w", encoding="utf-8") as f:
            json.dump(unique, f, indent=2, ensure_ascii=False)
            
        print(f"[+] Saved {len(unique)} cards to {target_rel}")

    # 3. Clean up old files
    print("\nCleaning up source files...")
    for sf in all_json_files:
        try:
            os.remove(sf)
        except Exception:
            pass

    # Clean up empty subdirectories
    for root, dirs, files in os.walk(DECKS_DIR, topdown=False):
        for d in dirs:
            dir_path = Path(root) / d
            try:
                # Remove if empty (will fail if not empty)
                os.rmdir(dir_path)
                print(f"[-] Removed empty directory: {dir_path.relative_to(DECKS_DIR)}")
            except Exception:
                pass

    print("\n=== DATABASE MIGRATION STEP 1 COMPLETE ===")

if __name__ == "__main__":
    migrate()
