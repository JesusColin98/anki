import json
import urllib.request
import urllib.error
import sys

def invoke(action, **params):
    payload = {'action': action, 'version': 6}
    if params:
        payload['params'] = params
    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8765', data=req_data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            if res.get('error') is not None:
                raise Exception(res['error'])
            return res['result']
    except urllib.error.URLError as e:
        print(f"Error connecting to AnkiConnect. Is Anki running?", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def ensure_model_exists():
    model_name = "Engaging_Cloze_Model"
    models = invoke('modelNames')
    if model_name in models:
        return
    print(f"Creating custom model '{model_name}'...")

# Philosophy Dataset
philosophy_cards = [
    # Beginner: Classical & Eastern
    {
        "deck": "Philosophy::01_Beginner::01_Classical_Foundations",
        "scenario": "Philosophy Beginner: Aristotelian Ethics 🏛️",
        "text": "Aristotle's ethical concept of the {{c1::Golden Mean}} (El Justo Medio) states that virtue is found by cultivating character traits that avoid the extremes of {{c1::excess}} and {{c1::deficiency}}.",
        "explanation": "Virtue is the balance point between two opposing vices. For example, Courage is the Golden Mean between Cowardice (deficiency of confidence) and Rashness (excess of confidence).",
        "usage": "To practice the Golden Mean, analyze your behaviors: do not act out of fear (deficiency) or act recklessly without thinking (excess), but act assertively and deliberately (mean).",
        "spanish": "El concepto ético de Aristóteles del Justo Medio establece que la virtud se encuentra al cultivar rasgos de carácter que evitan los extremos del exceso y la deficiencia."
    },
    {
        "deck": "Philosophy::01_Beginner::02_Eastern_Philosophies",
        "scenario": "Philosophy Beginner: Taoism ☯️",
        "text": "The core Taoist concept of {{c1::Wu Wei}} (non-action) refers to a state of alignment with the flow of life, acting effortlessly without {{c1::force or struggle}}.",
        "explanation": "Wu Wei does not mean laziness; it means acting in a way that is natural and fluid, like water flowing around obstacles, rather than fighting against them.",
        "usage": "Instead of forcing a conversation or trying to control a situation that isn't working, practice Wu Wei by stepping back and letting events develop naturally.",
        "spanish": "El concepto taoísta central de Wu Wei (no acción) se refiere a un estado de alineación con el flujo de la vida, actuando sin esfuerzo ni fuerza."
    },
    
    # Intermediate: Stoicism & Rationalism
    {
        "deck": "Philosophy::02_Intermediate::01_Stoicism",
        "scenario": "Philosophy Intermediate: Stoic Resilience 🧭",
        "text": "The Stoic {{c1::Dichotomy of Control}} separates the universe into things we can control (our {{c1::choices and judgments}}) and things we cannot (external events, past, others' opinions).",
        "explanation": "Epictetus argued that unhappiness comes from trying to control things that are external to us. Focusing only on our internal responses brings peace (ataraxia) and resilience.",
        "usage": "If your project deadline is delayed due to an external vendor, you cannot control the vendor (external), but you can control how you respond to the situation and adapt (internal).",
        "spanish": "La dicotomía del control estoica separa el universo en cosas que podemos controlar (nuestras elecciones y juicios) y cosas que no."
    },
    {
        "deck": "Philosophy::02_Intermediate::01_Stoicism",
        "scenario": "Philosophy Intermediate: Stoic Resilience 🧭",
        "text": "Marcus Aurelius described the {{c1::Inner Citadel}} as a mental fortress where one can retreat to find peace, protected from {{c1::external chaos and emotional turbulence}}.",
        "explanation": "The mind is a refuge. External events cannot touch it unless we allow them to by forming negative judgments about them.",
        "usage": "When surrounded by stress, noise, or criticism, retreat to your Inner Citadel by reminding yourself that others' opinions do not define your character.",
        "spanish": "Marco Aurelio describió la Ciudadela Interior como una fortaleza mental donde uno puede retirarse para encontrar paz, protegido del caos externo."
    },
    
    # Advanced: Modern & Postmodern
    {
        "deck": "Philosophy::03_Advanced::01_Modern_Postmodern",
        "scenario": "Philosophy Advanced: Existentialism 🎭",
        "text": "Jean-Paul Sartre's existentialist maxim {{c1::'existence precedes essence'}} states that humans exist first, and then define their purpose and identity through their {{c1::choices and actions}}.",
        "explanation": "There is no pre-defined human nature or destiny. We are completely free and responsible for who we become, which can cause existential dread (angst).",
        "usage": "You are not born a 'failure' or a 'hero'; you construct your identity daily through the commitments you choose to keep.",
        "spanish": "La máxima existencialista de Jean-Paul Sartre 'la existencia precede a la esencia' establece que los humanos existen primero y luego definen su propósito a través de sus elecciones."
    }
]

def create_philosophy_decks():
    ensure_model_exists()
    
    # Create decks
    deck_names = set(card['deck'] for card in philosophy_cards)
    for deck in deck_names:
        print(f"Ensuring deck '{deck}' exists...")
        invoke('createDeck', deck=deck)
        
    print("\nAdding philosophy cards...")
    notes = []
    for card in philosophy_cards:
        note = {
            "deckName": card['deck'],
            "modelName": "Engaging_Cloze_Model",
            "fields": {
                "Text": card['text'],
                "Scenario": card['scenario'],
                "Explanation": card['explanation'],
                "Usage_Examples": card['usage'],
                "Spanish_Translation": card['spanish'],
                "Audio": ""
            },
            "options": {
                "allowDuplicate": True
            },
            "tags": ["philosophy_path", card['deck'].split("::")[-1].lower()]
        }
        notes.append(note)
        
    result = invoke('addNotes', notes=notes)
    print(f"\nSuccessfully added {len(result)} philosophy cards!")
    for note_id, card in zip(result, philosophy_cards):
        print(f" - Added card '{card['text'][:45]}...' (Note ID: {note_id})")

if __name__ == "__main__":
    create_philosophy_decks()
