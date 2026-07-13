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
    # Model template fallback
    print(f"Creating custom model '{model_name}'...")

# Languages Path Dataset
lang_cards = [
    # German
    {
        "deck": "German::01_A1_Beginner::01_Greetings_and_Farewells",
        "scenario": "German A1: Greetings 🇩🇪",
        "text": "In a business setting or with strangers, you should greet them formally with: '{{c1::Guten Morgen}}' (until 11 AM) or '{{c1::Guten Tag}}' (11 AM to 6 PM).",
        "explanation": "German distinguishes strictly between formal and informal greetings. Formal greetings are used with the pronoun 'Sie' and change based on the time of day.",
        "usage": "Time-based formal greetings:<ul><li><code>Guten Morgen</code> (Good morning - until 11 AM)</li><li><code>Guten Tag</code> (Good day - 11 AM to 6 PM)</li><li><code>Guten Abend</code> (Good evening - after 6 PM)</li></ul>",
        "spanish": "En un ámbito empresarial o con extraños, debes saludarlos formalmente con: 'Guten Morgen' (hasta las 11 AM) o 'Guten Tag' (de 11 AM a 6 PM)."
    },
    {
        "deck": "German::01_A1_Beginner::01_Greetings_and_Farewells",
        "scenario": "German A1: Greetings 🇩🇪",
        "text": "To ask a stranger 'How are you?' formally in German, you say: '{{c1::Wie geht es Ihnen?}}'",
        "explanation": "<strong>Ihnen</strong> is the dative case of the formal pronoun 'Sie'. For friends or peers, you would use the informal 'Wie geht es dir?' or simply 'Wie geht's?'.",
        "usage": "Usage examples:<ul><li>Formal: <code>Wie geht es Ihnen, Herr Müller?</code> (How are you, Mr. Müller?)</li><li>Informal: <code>Wie geht es dir, Anna?</code> (How are you, Anna?)</li></ul>",
        "spanish": "Para preguntar formalmente a un extraño '¿Cómo está usted?' en alemán, dices: 'Wie geht es Ihnen?'."
    },
    {
        "deck": "German::01_A1_Beginner::01_Greetings_and_Farewells",
        "scenario": "German A1: Goodbyes 🇩🇪",
        "text": "A common informal way to say goodbye to friends in German is '{{c1::Tschüss}}' or '{{c1::Bis bald}}' (See you soon).",
        "explanation": "<strong>Tschüss</strong> is the most common informal goodbye in Germany. <strong>Auf Wiedersehen</strong> is formal and used in shops, business meetings, or with strangers.",
        "usage": "Goodbye options:<ul><li>Informal: <code>Tschüss!</code> (Bye!) or <code>Bis später!</code> (See you later!)</li><li>Formal: <code>Auf Wiedersehen!</code> (Goodbye!)</li></ul>",
        "spanish": "Una forma informal común de despedirse de los amigos en alemán es 'Tschüss' o 'Bis bald' (Hasta pronto)."
    },
    
    # French
    {
        "deck": "French::01_A1_Beginner::01_Greetings_and_Farewells",
        "scenario": "French A1: Greetings 🇫🇷",
        "text": "When entering a French bakery at 7:00 PM, you should greet the staff with '{{c1::Bonsoir}}' instead of 'Bonjour'.",
        "explanation": "<strong>Bonjour</strong> is used during the day (Hello/Good morning). <strong>Bonsoir</strong> is used after 6 PM (Good evening). Saying 'Bonjour' late in the evening sounds unnatural in France.",
        "usage": "Time guidelines:<ul><li><code>Bonjour</code> (used from morning until approximately 6 PM)</li><li><code>Bonsoir</code> (used after 6 PM)</li></ul>",
        "spanish": "Al entrar a una panadería francesa a las 7:00 PM, debes saludar al personal con 'Bonsoir' en lugar de 'Bonjour'."
    },
    {
        "deck": "French::01_A1_Beginner::01_Greetings_and_Farewells",
        "scenario": "French A1: Greetings 🇫🇷",
        "text": "To ask a stranger or colleague 'How are you?' formally in French, you say: '{{c1::Comment allez-vous ?}}'",
        "explanation": "<strong>vous</strong> is the formal pronoun of respect. For friends or children, you use the informal 'Ça va ?' or 'Comment tu vas ?'.",
        "usage": "Pronunciation tip: Pronounce the 't' in 'Comment' linked with 'allez' as a 't' sound: <code>Comment allez-vous ?</code> (/kɔ.mɑ̃.t‿a.le.vu/).<ul><li>Formal: <code>Bonjour Madame, comment allez-vous ?</code></li><li>Informal: <code>Salut Marc, ça va ?</code></li></ul>",
        "spanish": "Para preguntar formalmente a un extraño o colega '¿Cómo está usted?' en francés, dices: 'Comment allez-vous ?'."
    },
    {
        "deck": "French::01_A1_Beginner::01_Greetings_and_Farewells",
        "scenario": "French A1: Greetings 🇫🇷",
        "text": "In French, the informal word '{{c1::Salut}}' can be used to say both 'Hi' and 'Bye'.",
        "explanation": "<strong>Salut</strong> is a highly versatile informal greeting. It should only be used with friends, family, or people you know well.",
        "usage": "Usage scenarios:<ul><li>Arriving: <code>Salut, ça va ?</code> (Hi, how's it going?)</li><li>Leaving: <code>Allez, salut !</code> (Okay, bye!)</li></ul>",
        "spanish": "En francés, la palabra informal 'Salut' se puede usar tanto para decir 'Hola' como 'Adiós'."
    }
]

def create_lang_decks_and_cards():
    ensure_model_exists()
    
    # Create decks
    deck_names = set(card['deck'] for card in lang_cards)
    for deck in deck_names:
        print(f"Ensuring deck '{deck}' exists...")
        invoke('createDeck', deck=deck)
        
    print("\nAdding German & French A1 cards...")
    notes = []
    for card in lang_cards:
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
            "tags": ["languages_path", "A1", card['deck'].split("::")[-1].lower()]
        }
        notes.append(note)
        
    result = invoke('addNotes', notes=notes)
    print(f"\nSuccessfully added {len(result)} language cards!")
    for note_id, card in zip(result, lang_cards):
        print(f" - Added card '{card['text'][:45]}...' (Note ID: {note_id})")

if __name__ == "__main__":
    create_lang_decks_and_cards()
