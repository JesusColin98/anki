import time
import requests
import json

OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"
model = "qwen2.5:14b"

def test_ollama():
    sample_cards = [
        {"term": "Finitude", "definition": "The fundamental human condition of having limited time, energy, and control, which modern productivity culture often attempts to deny or overcome."},
        {"term": "Time as a Resource", "definition": "The modern paradigm where time is viewed as an abstract, measurable commodity to be optimized, rather than the natural medium in which life unfolds."},
        {"term": "The Conveyor Belt Metaphor", "definition": "A way to visualize the modern anxiety of time: treating passing hours as empty containers that must be filled with productive activities to avoid feelings of waste or guilt."}
    ]
    
    system_instruction = (
        "You are an expert Anki card generator. Convert the input cards into structured JSON format matching this schema:\n"
        "[\n"
        "  {\n"
        "    \"deck\": \"<Pillars::Category::Subcategory::DeckName>\",\n"
        "    \"scenario\": \"<Categoría Corta>: <Contexto o Situación con Emoji>\",\n"
        "    \"text\": \"Oración principal con exactamente un {{c1::<Concepto Clave>}} enfocado.\",\n"
        "    \"explanation\": \"Desglose conceptual intuitivo de 2 a 3 oraciones respondiendo por qué funciona.\",\n"
        "    \"usage\": \"<ul><li><b>Punto clave 1</b>: ...</li><li><b>Punto clave 2</b>: ...</li></ul>\",\n"
        "    \"spanish\": \"Traducción completa y natural al español.\",\n"
        "    \"tags\": [\"tag1\", \"tag2\"]\n"
        "  }\n"
        "]\n"
        "Return ONLY the raw JSON array. Do not wrap in markdown code blocks."
    )
    
    user_prompt = f"Convert these 3 cards for the book 'Four Thousand Weeks' under deck '06_Business_and_Productivity::Books_Path::Productivity::03_Learning_Productivity':\n{json.dumps(sample_cards, indent=2)}"
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.1,
    }
    
    t0 = time.time()
    try:
        resp = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        t1 = time.time()
        print(f"Time taken: {t1-t0:.2f} seconds")
        print("Response:")
        print(content)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_ollama()
