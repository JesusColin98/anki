#!/usr/bin/env python3
"""Agentic Generator-Evaluator Loop for Anki Cards.

Supports both Gemini API and Local Ollama models.
Includes a benchmarking mode to evaluate local models.
"""

import argparse
import json
import time
from typing import List, Dict, Any, Tuple, Optional

from generator import RULE_CATALOG, call_gemini, render_t9_card, render_t8_card
from card_validator import sanitize_and_validate_card
from local_ollama_provider import chat_completion

EVALUATOR_SYSTEM_PROMPT = """\
You are an expert Anki card Quality Assurance (QA) evaluator.
Your job is to strictly evaluate a batch of JSON Anki cards against specific rules.
You must output a JSON object with two fields:
- "accepted": true if all cards follow the rules perfectly, false if there are violations.
- "feedback": "Detailed feedback on what is wrong and how to fix it, or 'All good' if accepted."

EVALUATION CRITERIA:
1. Atomicity: Each card must test exactly one concept (max 1 cloze deletion).
2. The rules in 'rules_applied' must actually be present in the 'connected_form'.
3. The 'spanish' translation must be natural.
4. If it's a T9_ListeningChunk card, the 'connected_form' must represent fast natural speech.
5. Do NOT accept cards that just have simple dictionary pronunciations for connected speech rules.

OUTPUT FORMAT:
{"accepted": true, "feedback": "Looks good"}
"""

def generate_with_provider(provider: str, model: str, system_prompt: str, user_prompt: str) -> Optional[List[Dict]]:
    """Generates cards using the specified provider."""
    print(f"    [Generation] Using {provider} ({model})...")
    if provider == "gemini":
        response = call_gemini(system_prompt, user_prompt)
        if response and "cards" in response:
            return response["cards"]
        return response if isinstance(response, list) else []
    elif provider == "ollama":
        content = chat_completion(system_prompt, user_prompt, model, response_format={"type": "json_object"})
        if content:
            try:
                data = json.loads(content)
                return data.get("cards", data) if isinstance(data, dict) else data
            except Exception as e:
                print(f"    [!] Failed to parse generator JSON: {e}")
    return None

def evaluate_with_provider(provider: str, model: str, rule_prompt: str, cards_json: str) -> Tuple[bool, str]:
    """Evaluates generated cards using the specified provider."""
    print(f"    [Evaluation] Using {provider} ({model})...")
    eval_user_prompt = f"""
    Please evaluate these generated Anki cards.
    
    ORIGINAL GENERATION RULE:
    {rule_prompt}
    
    GENERATED CARDS (JSON):
    {cards_json}
    
    Provide your evaluation in the required JSON format.
    """
    
    if provider == "gemini":
        response = call_gemini(EVALUATOR_SYSTEM_PROMPT, eval_user_prompt)
        if response and isinstance(response, dict):
            return response.get("accepted", False), response.get("feedback", "No feedback")
        return False, "Failed to parse Gemini evaluation"
    elif provider == "ollama":
        content = chat_completion(EVALUATOR_SYSTEM_PROMPT, eval_user_prompt, model, response_format={"type": "json_object"})
        if content:
            try:
                data = json.loads(content)
                return data.get("accepted", False), data.get("feedback", "No feedback")
            except Exception as e:
                return False, f"Failed to parse Evaluator JSON: {e}"
    return False, "Provider not supported for evaluation."

def run_agentic_loop(
    rule_num: int, 
    count: int, 
    provider: str = "ollama", 
    gen_model: str = "qwen2.5:14b", 
    eval_model: str = "qwen2.5:14b",
    max_retries: int = 3
) -> Tuple[bool, List[Dict], int, float]:
    """Runs the full Q loop: Generate -> Deterministic Validate -> LLM Evaluate."""
    if rule_num not in RULE_CATALOG:
        print(f"[-] Unknown rule {rule_num}")
        return False, [], 0, 0.0

    info = RULE_CATALOG[rule_num]
    base_user_prompt = info["user_prompt"].format(count=count)
    system_prompt = info["system_prompt"]
    
    current_user_prompt = base_user_prompt
    start_time = time.time()
    
    for attempt in range(1, max_retries + 1):
        print(f"\n--- ATTEMPT {attempt}/{max_retries} ---")
        
        # 1. Generation Phase
        raw_cards = generate_with_provider(provider, gen_model, system_prompt, current_user_prompt)
        if not raw_cards or not isinstance(raw_cards, list):
            print("    [!] Generation failed or returned empty.")
            current_user_prompt = base_user_prompt + "\n\nFEEDBACK FROM PREVIOUS ATTEMPT: You returned invalid JSON or an empty list. Please return a valid JSON array of cards."
            continue
            
        print(f"    [+] Generated {len(raw_cards)} cards.")
        
        # 2. Deterministic Validation Phase
        rendered = []
        det_errors = []
        import uuid
        for raw in raw_cards:
            try:
                card = render_t8_card(raw, info) if info["template"] == "T8_MinimalPair" else render_t9_card(raw, info)
                
                # Wrap flat card into NestedSchema to pass validation
                nested_card = {
                    "id": str(uuid.uuid4())[:8],
                    "deck": card.get("deck", info["deck"]),
                    "template": info["template"],
                    "metadata": {
                        "difficulty": "intermediate",
                        "pillar": "03_Languages",
                        "tags": card.get("tags", [])
                    },
                    "content": raw
                }
                
                is_valid, cleaned, errs = sanitize_and_validate_card(nested_card)
                if not is_valid:
                    det_errors.extend(errs)
                else:
                    rendered.append(cleaned)
            except Exception as e:
                det_errors.append(f"Rendering exception: {e}")
                
        if det_errors:
            print(f"    [!] Deterministic validation failed with {len(det_errors)} errors.")
            print(f"        First error: {det_errors[0]}")
            feedback = f"Your previous output failed deterministic schema validation. Fix these errors:\n" + "\n".join(det_errors[:3])
            current_user_prompt = base_user_prompt + f"\n\nCRITICAL FEEDBACK FROM VALIDATOR:\n{feedback}"
            continue
            
        if not rendered:
            print("    [!] No valid cards after rendering.")
            continue
            
        print(f"    [✓] Deterministic validation passed for {len(rendered)} cards.")
        
        # 3. LLM Evaluation Phase
        cards_json = json.dumps(raw_cards, indent=2, ensure_ascii=False)
        accepted, feedback = evaluate_with_provider(provider, eval_model, base_user_prompt, cards_json)
        
        if accepted:
            print(f"    [✓] Evaluator ACCEPTED the cards! Feedback: {feedback}")
            elapsed = time.time() - start_time
            return True, rendered, attempt, elapsed
        else:
            print(f"    [!] Evaluator REJECTED the cards. Feedback: {feedback}")
            current_user_prompt = base_user_prompt + f"\n\nCRITICAL FEEDBACK FROM QA EVALUATOR:\n{feedback}\n\nPlease regenerate the cards fixing these exact issues."
            
    elapsed = time.time() - start_time
    print(f"\n[-] Exhausted {max_retries} retries.")
    return False, [], max_retries, elapsed

def cmd_benchmark(rule_num: int, count: int, models: List[str]):
    print(f"\n========== BENCHMARKING MODELS ==========")
    print(f"Rule: {rule_num}, Cards: {count}")
    print(f"Models: {models}\n")
    
    results = []
    
    for model in models:
        print(f"\n{'='*40}")
        print(f"EVALUATING MODEL: {model}")
        print(f"{'='*40}")
        
        provider = "gemini" if "gemini" in model.lower() else "ollama"
        success, cards, attempts, elapsed = run_agentic_loop(
            rule_num=rule_num,
            count=count,
            provider=provider,
            gen_model=model,
            eval_model=model,
            max_retries=3
        )
        
        results.append({
            "model": model,
            "success": success,
            "attempts": attempts,
            "elapsed": elapsed,
            "valid_cards_produced": len(cards)
        })
        
    print("\n========== BENCHMARK RESULTS ==========")
    print(f"{'Model':<20} | {'Status':<10} | {'Attempts':<10} | {'Time (s)':<10} | {'Cards'}")
    print("-" * 70)
    for res in results:
        status = "PASSED" if res["success"] else "FAILED"
        print(f"{res['model']:<20} | {status:<10} | {res['attempts']:<10} | {res['elapsed']:<10.2f} | {res['valid_cards_produced']}")
        
def main():
    parser = argparse.ArgumentParser(description="Agentic Generator-Evaluator Loop")
    parser.add_argument("--rule", type=int, default=2, help="Rule number (0-18)")
    parser.add_argument("--count", type=int, default=3, help="Number of cards to generate")
    parser.add_argument("--provider", choices=["ollama", "gemini"], default="ollama", help="API Provider")
    parser.add_argument("--gen-model", type=str, default="qwen2.5:14b", help="Model for generation")
    parser.add_argument("--eval-model", type=str, default="qwen2.5:14b", help="Model for evaluation")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark mode")
    parser.add_argument("--models", type=str, nargs="+", default=["qwen2.5:14b", "qwen2.5:14b-optimized", "gemma2:9b"], help="List of models for benchmark")
    
    args = parser.parse_args()
    
    if args.benchmark:
        cmd_benchmark(args.rule, args.count, args.models)
    else:
        print(f"Starting single run with Provider: {args.provider}, Gen: {args.gen_model}, Eval: {args.eval_model}")
        success, cards, attempts, elapsed = run_agentic_loop(
            rule_num=args.rule,
            count=args.count,
            provider=args.provider,
            gen_model=args.gen_model,
            eval_model=args.eval_model
        )
        if success:
            print(f"\n[✓] Success after {attempts} attempts in {elapsed:.1f} seconds. {len(cards)} valid cards generated.")
        else:
            print(f"\n[-] Failed after {attempts} attempts in {elapsed:.1f} seconds.")

if __name__ == "__main__":
    main()
