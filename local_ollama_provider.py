#!/usr/bin/env python3
"""Local LLM Provider (Ollama API Wrapper) for Anki Card Generation.

Enables offline / generic card generation using local models (Gemma 2, Llama 3)
via Ollama's OpenAI-compatible API endpoint (http://localhost:11434/v1).
"""

import json

import requests

OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"


def chat_completion(
    system_prompt: str,
    user_prompt: str,
    model: str = "gemma2:9b",
    response_format: dict = None,
) -> str:
  """Calls local Ollama instance and returns the raw string response."""
  payload = {
      "model": model,
      "messages": [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": user_prompt},
      ],
      "temperature": 0.2,
  }
  if response_format:
    payload["response_format"] = response_format

  try:
    resp = requests.post(OLLAMA_API_URL, json=payload, timeout=90)
    resp.raise_for_status()
    result = resp.json()
    return result["choices"][0]["message"]["content"]
  except requests.exceptions.ConnectionError:
    print(
        f"[-] Note: Could not connect to local Ollama server at {OLLAMA_API_URL}."
    )
    print(f"    Make sure Ollama is running (`ollama serve` and `ollama run {model}`).")
    return None
  except requests.exceptions.Timeout:
    print(f"[-] Timeout error waiting for local model {model}")
    return None
  except Exception as e:
    print(f"[-] Local LLM error: {e}")
    return None


def generate_anki_cards_local(
    prompt_text: str,
    deck_name: str = "Local_Generated::General",
    model: str = "gemma2:9b",
) -> list:
  """Calls local Ollama instance to generate structured Anki cards."""
  system_instruction = (
      "You are an expert Anki card generator. Return ONLY a JSON array of card"
      " objects. Each card must have: 'deck', 'scenario', 'text' (with {{c1::}})"
      " 'explanation', 'usage', 'spanish', 'tags'."
  )

  user_prompt = f"""
  Generate 3 high-quality Anki Cloze deletion cards for the following content:
  ---
  {prompt_text}
  ---
  Deck Name: {deck_name}
  """

  print(f"[+] Invoking local model '{model}' at {OLLAMA_API_URL}...")
  content = chat_completion(
      system_instruction, 
      user_prompt, 
      model, 
      response_format={"type": "json_object"}
  )
  
  if not content:
    return []

  try:
    data = json.loads(content)
    cards = data.get("cards", data) if isinstance(data, dict) else data
    return cards if isinstance(cards, list) else []
  except Exception as e:
    print(f"[-] JSON parse error: {e}")
    return []


if __name__ == "__main__":
  sample_text = (
      "Active recall is a principle of efficient learning, which claims the"
      " entity needs to be frequently tested for memory retention."
  )
  cards = generate_anki_cards_local(sample_text)
  print(f"Result: {json.dumps(cards, indent=2, ensure_ascii=False)}")
