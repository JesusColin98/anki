import os
import sys
import json
from pathlib import Path

# Add parent directory to sys.path to import template_engine
SCRATCH_DIR = Path(__file__).resolve().parent
PARENT_DIR = SCRATCH_DIR.parent
sys.path.append(str(PARENT_DIR))

from template_engine import build_card

DECKS_DIR = PARENT_DIR / "decks"

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_json(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def rebuild_index():
    index_path = DECKS_DIR / "index.json"
    decks_list = []
    total_cards = 0
    
    for root, _, files in os.walk(DECKS_DIR):
        for file in sorted(files):
            if file.endswith(".json") and file != "index.json":
                file_path = Path(root) / file
                rel_path = os.path.relpath(file_path, DECKS_DIR)
                derived_deck = str(Path(rel_path).with_suffix("")).replace(os.sep, "::")
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        cards = json.load(f)
                    
                    decks_list.append({
                        "deck": derived_deck,
                        "path": f"decks/{rel_path.replace(os.sep, '/')}",
                        "cards_count": len(cards)
                    })
                    total_cards += len(cards)
                except Exception as e:
                    print(f"Error reading {file_path} for index rebuild: {e}")
                    
    decks_list.sort(key=lambda x: x["deck"])
    
    index_data = {
        "total_cards": total_cards,
        "total_decks": len(decks_list),
        "decks": decks_list
    }
    
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    print(f"\nRebuilt index with {len(decks_list)} decks and {total_cards} total cards.")

# ----------------- Drills Definition -----------------

drills_to_add = [
    # 1. English (Connected Speech) - 6 Drills
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "rule_name": "Flap T",
        "formal_phrase": "Put it in a bottle of water.",
        "fast_pronunciation": "Pu-di-tin a bo-dle of wa-der.",
        "explanation": "The /t/ sounds are located between vowels in unstressed syllables. They tap against the alveolar ridge, sounding like a Spanish 'r' or light 'd', linking all words together.",
        "spanish": "Ponlo en una botella de agua."
    },
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "rule_name": "Nasal T-Deletion",
        "formal_phrase": "The international center has twenty computers.",
        "fast_pronunciation": "The innernational cener has tweny computers.",
        "explanation": "Unstressed /t/ directly following /n/ is omitted because the nasal articulation dominates at the alveolar ridge, letting speakers skip the stop sound.",
        "spanish": "El centro internacional tiene veinte computadoras."
    },
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "rule_name": "Linking and Intrusive R",
        "formal_phrase": "I have no idea of the law and order.",
        "fast_pronunciation": "I have no idea-r-of the law-r-and order.",
        "explanation": "In non-rhotic accents, an 'r' sound is inserted to bridge contiguous vowel sounds, preventing a glottal break (hiatus).",
        "spanish": "No tengo idea de la ley y el orden."
    },
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "rule_name": "Glottal Stop",
        "formal_phrase": "I can't go to the football match.",
        "fast_pronunciation": "I can' ɡo to the foo'ball match.",
        "explanation": "Before another consonant, final /t/ is not released with air; instead, the airflow is cut off briefly in the glottis (throat).",
        "spanish": "No puedo ir al partido de fútbol."
    },
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "rule_name": "Unreleased Stops",
        "formal_phrase": "Drop it in the hot dog bag.",
        "fast_pronunciation": "Drop-it in the hah-dog bag.",
        "explanation": "The final stop consonants /p/, /t/, and /g/ are unreleased (held), cutting off the vowels abruptly without a puff of air.",
        "spanish": "Déjalo en la bolsa de los perros calientes."
    },
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "rule_name": "Advanced Auxiliary Chunks",
        "formal_phrase": "What did you do? Did you ever think it would have been easy?",
        "fast_pronunciation": "Whadja do? Jever think it woulda bin easy?",
        "explanation": "The auxiliary sequences compress heavily via coalescence (what did you &rarr; whadja; did you &rarr; jever) and reduction (would have &rarr; woulda).",
        "spanish": "¿Qué hiciste? ¿Alguna vez pensaste que habría sido fácil?"
    },

    # 2. Spanish - 4 Drills
    {
        "deck": "03_Languages::Spanish::Phonetics::General",
        "rule_name": "Sinalefa",
        "formal_phrase": "Mi hijo va de una vez a la escuela.",
        "fast_pronunciation": "Mijo va duna vez a la escuela.",
        "explanation": "Contiguous vowels 'i-hi' and 'de-u' merge into single syllables in fast speech, eliminating word boundaries.",
        "spanish": "My son goes to school at once."
    },
    {
        "deck": "03_Languages::Spanish::Phonetics::General",
        "rule_name": "Aspiración de S",
        "formal_phrase": "Los mismos muchachos están listos.",
        "fast_pronunciation": "Lo' mi'mo' muchachos ehta' liht-o'.",
        "explanation": "Syllable-final 's' is aspirated to a soft breath [h] or dropped entirely in fast conversational dialects.",
        "spanish": "The same boys are ready."
    },
    {
        "deck": "03_Languages::Spanish::Phonetics::General",
        "rule_name": "Relajación de D",
        "formal_phrase": "Está cansado de trabajar para nada.",
        "fast_pronunciation": "Está cansao de trabajar pa' na'.",
        "explanation": "The dental consonant /d/ between vowels is extremely relaxed, resulting in complete deletion in colloquial fast speech.",
        "spanish": "He is tired of working for nothing."
    },
    {
        "deck": "03_Languages::Spanish::Phonetics::General",
        "rule_name": "Asimilación N-M",
        "formal_phrase": "Dame un beso en mi mejilla.",
        "fast_pronunciation": "Dame um beso em mi mejilla.",
        "explanation": "The nasal /n/ shifts its place of articulation to bilabial [m] before the upcoming bilabial consonants /b/ and /m/.",
        "spanish": "Give me a kiss on my cheek."
    },

    # 3. Chinese - 3 Drills
    {
        "deck": "03_Languages::Chinese::Phonetics::General",
        "rule_name": "Erhua (儿化)",
        "formal_phrase": "我们在玩儿呢 (Women zai wan er ne).",
        "fast_pronunciation": "Women zai waer ne.",
        "explanation": "The retroflex suffix blends with the final vowel of 'wan', dropping the nasal 'n' and adding r-coloring.",
        "spanish": "Estamos jugando aquí."
    },
    {
        "deck": "03_Languages::Chinese::Phonetics::General",
        "rule_name": "Neutral Tone (轻声)",
        "formal_phrase": "这是什么？ (Zhe shi shen me?)",
        "fast_pronunciation": "Zhe shi shenme?",
        "explanation": "The second character 'me' loses its original tone, becoming short, flat, and soft.",
        "spanish": "¿Qué es esto?"
    },
    {
        "deck": "03_Languages::Chinese::Phonetics::General",
        "rule_name": "Syllable Contraction",
        "formal_phrase": "我不知道 (Wo bu zhi dao).",
        "fast_pronunciation": "Wo buzdao.",
        "explanation": "The adjacent syllables 'bu', 'zhi', and 'dao' merge into 'buzdao' by dropping the retroflex initial /zh/.",
        "spanish": "No lo sé."
    },

    # 4. French - 3 Drills
    {
        "deck": "03_Languages::French::Phonetics::General",
        "rule_name": "La Liaison",
        "formal_phrase": "Nous avons des enfants.",
        "fast_pronunciation": "Nou-zavon de-zanfan.",
        "explanation": "The normally silent final 's' in 'nous' and 'des' is voiced as [z] and links directly to the initial vowels.",
        "spanish": "Tenemos niños."
    },
    {
        "deck": "03_Languages::French::Phonetics::General",
        "rule_name": "Elision of E Muet",
        "formal_phrase": "Je ne sais pas quoi faire.",
        "fast_pronunciation": "J'sais pas quoi faire.",
        "explanation": "The mute 'e' in 'ne' is dropped, creating a consonant cluster /ʒs/ which assimilates to voiceless [ʃs] ('sh-pais').",
        "spanish": "No sé qué hacer."
    },
    {
        "deck": "03_Languages::French::Phonetics::General",
        "rule_name": "Pronoun Compression",
        "formal_phrase": "Il y a un problème.",
        "fast_pronunciation": "Y'a un problème.",
        "explanation": "The pronoun sequence 'il y a' is compressed to the single syllable 'y'a' (/ja/) in conversational speech.",
        "spanish": "Hay un problema."
    },

    # 5. German - 3 Drills
    {
        "deck": "03_Languages::German::Phonetics::General",
        "rule_name": "Auslautverhärtung",
        "formal_phrase": "Der Hund war den ganzen Tag aktiv.",
        "fast_pronunciation": "Der Hunt war den ganzen Taak aktif.",
        "explanation": "Voiced consonants /d/ in 'Hund', /g/ in 'Tag', and /v/ in 'aktiv' are devoiced to [t], [k], and [f] at syllable endings.",
        "spanish": "El perro estuvo activo todo el día."
    },
    {
        "deck": "03_Languages::German::Phonetics::General",
        "rule_name": "Knacklaut (Glottal Stop)",
        "formal_phrase": "Ich esse einen Apfel.",
        "fast_pronunciation": "Ich [ʔ]esse [ʔ]einen [ʔ]Apfel.",
        "explanation": "A glottal stop [ʔ] is inserted before each word-initial vowel, separating the words sharply.",
        "spanish": "Como una manzana."
    },
    {
        "deck": "03_Languages::German::Phonetics::General",
        "rule_name": "Reduction of final -en",
        "formal_phrase": "Wir kommen morgen.",
        "fast_pronunciation": "Wir komm'n morg'n.",
        "explanation": "The final unstressed '-en' syllables lose their vowels, leaving a syllabic nasal [n̩].",
        "spanish": "Venimos mañana."
    },

    # 6. Italian - 2 Drills
    {
        "deck": "03_Languages::Italian::Phonetics::General",
        "rule_name": "Raddoppiamento Fonosintattico",
        "formal_phrase": "Andiamo a casa per un caffè espresso.",
        "fast_pronunciation": "Andiamo a-ccasa per un caffè m-espresso.",
        "explanation": "The stressed vowels in 'a' and 'caffè' trigger double pronunciation of the next word's initial consonant.",
        "spanish": "Vamos a casa por un café expreso."
    },
    {
        "deck": "03_Languages::Italian::Phonetics::General",
        "rule_name": "Troncamento",
        "formal_phrase": "Buon giorno, un poco di pane, per favore.",
        "fast_pronunciation": "Buongiorno, un po' di pane, per favore.",
        "explanation": "Vowels at the end of 'buono' and 'poco' are dropped, creating shorter, more fluid phrases.",
        "spanish": "Buenos días, un poco de pan, por favor."
    },

    # 7. Portuguese - 3 Drills
    {
        "deck": "03_Languages::Portuguese::Phonetics::General",
        "rule_name": "Palatalization of T/D (BR)",
        "formal_phrase": "Bom dia, tia.",
        "fast_pronunciation": "Bom djia, tchia.",
        "explanation": "In Brazilian Portuguese, /d/ and /t/ are palatalized into affricates [dʒ] and [tʃ] when preceding the vowel /i/.",
        "spanish": "Buenos días, tía."
    },
    {
        "deck": "03_Languages::Portuguese::Phonetics::General",
        "rule_name": "L-Vocalization (BR)",
        "formal_phrase": "O Brasil ganhou sob o sol.",
        "fast_pronunciation": "O Brasiw ganhou sob o sow.",
        "explanation": "Syllable-final L is vocalized to the semivowel [w] in Brazilian dialects.",
        "spanish": "Brasil ganó bajo el sol."
    },
    {
        "deck": "03_Languages::Portuguese::Phonetics::General",
        "rule_name": "Vowel Reduction (PT)",
        "formal_phrase": "Isto é excelente.",
        "fast_pronunciation": "Isto é shs-lẽt.",
        "explanation": "In European Portuguese, unstressed vowels are almost completely deleted, leaving consonant clusters.",
        "spanish": "Esto es excelente."
    },

    # 8. Japanese - 3 Drills
    {
        "deck": "03_Languages::Japanese::Phonetics::General",
        "rule_name": "Vowel Devoicing",
        "formal_phrase": "好きです (Suki desu).",
        "fast_pronunciation": "S-ki des'.",
        "explanation": "High vowels /u/ and /i/ lose their voicing between voiceless consonants /s/, /k/, /t/.",
        "spanish": "Me gusta / Es así."
    },
    {
        "deck": "03_Languages::Japanese::Phonetics::General",
        "rule_name": "Sokuon (促音)",
        "formal_phrase": "ちょっと待ってください (Chotto matte kudasai).",
        "fast_pronunciation": "Chotto ma[pause]te kudasai.",
        "explanation": "The small tsu represents a one-mora silent pause, holding the breath before the /t/ sound.",
        "spanish": "Espere un momento, por favor."
    },
    {
        "deck": "03_Languages::Japanese::Phonetics::General",
        "rule_name": "Colloquial Contractions",
        "formal_phrase": "食べてしまった (Tabete shimatta).",
        "fast_pronunciation": "Tabetchatta.",
        "explanation": "The auxiliary verb ending '-te shimatta' fuses and contracts into '-tchatta' in casual speech.",
        "spanish": "Terminé comiéndolo."
    },

    # 9. Hindi - 3 Drills
    {
        "deck": "03_Languages::Hindi::Phonetics::General",
        "rule_name": "Schwa Deletion",
        "formal_phrase": "यह खबर है (Yeh khabara hai).",
        "fast_pronunciation": "Yeh khabr hai.",
        "explanation": "The final implicit schwa vowel in 'khabara' is dropped, creating a consonant blend 'khabr'.",
        "spanish": "Esta es la noticia."
    },
    {
        "deck": "03_Languages::Hindi::Phonetics::General",
        "rule_name": "Aspirated 'H' Elision",
        "formal_phrase": "जल्दी कहना, बहुत अच्छा है (Jaldi kahana, bahut accha hai).",
        "fast_pronunciation": "Jaldi kana, baut accha hai.",
        "explanation": "The soft /h/ in 'kahana' and 'bahut' is dropped in fast conversation, fusing surrounding vowels.",
        "spanish": "Dilo rápido, es muy bueno."
    },
    {
        "deck": "03_Languages::Hindi::Phonetics::General",
        "rule_name": "Postposition Merger",
        "formal_phrase": "इस में देखो (Is me dekho).",
        "fast_pronunciation": "Isme dekho.",
        "explanation": "The pronoun 'is' and postposition 'me' fuse into a single rhythmic word 'isme'.",
        "spanish": "Mira dentro de esto."
    }
]

def run():
    print("=== GENERATING PRONUNCIATION DRILL CARDS ===")
    
    # We group card entries by target file path
    file_map = {
        "03_Languages::English::Phonetics::Connected_Speech": DECKS_DIR / "03_Languages" / "English" / "Phonetics" / "Connected_Speech.json",
        "03_Languages::Spanish::Phonetics::General": DECKS_DIR / "03_Languages" / "Spanish" / "Phonetics" / "General.json",
        "03_Languages::Chinese::Phonetics::General": DECKS_DIR / "03_Languages" / "Chinese" / "Phonetics" / "General.json",
        "03_Languages::French::Phonetics::General": DECKS_DIR / "03_Languages" / "French" / "Phonetics" / "General.json",
        "03_Languages::German::Phonetics::General": DECKS_DIR / "03_Languages" / "German" / "Phonetics" / "General.json",
        "03_Languages::Italian::Phonetics::General": DECKS_DIR / "03_Languages" / "Italian" / "Phonetics" / "General.json",
        "03_Languages::Portuguese::Phonetics::General": DECKS_DIR / "03_Languages" / "Portuguese" / "Phonetics" / "General.json",
        "03_Languages::Japanese::Phonetics::General": DECKS_DIR / "03_Languages" / "Japanese" / "Phonetics" / "General.json",
        "03_Languages::Hindi::Phonetics::General": DECKS_DIR / "03_Languages" / "Hindi" / "Phonetics" / "General.json",
    }
    
    grouped_cards = {}
    for entry in drills_to_add:
        deck_name = entry["deck"]
        if deck_name not in grouped_cards:
            grouped_cards[deck_name] = []
        # Render the card using the newly added T7_Pronunciation template!
        rendered = build_card("T7_Pronunciation", entry)
        grouped_cards[deck_name].append(rendered)
        
    for deck_name, rendered_list in grouped_cards.items():
        file_path = file_map[deck_name]
        existing_data = load_json(file_path)
        
        # Clean up any previously inserted broken cards containing single brace {c1::
        cleaned_existing_data = []
        for card in existing_data:
            # Check if it has the broken cloze syntax we just fixed
            if "Connected speech pronunciation: {c1::" in card.get("text", ""):
                print(f"Cleaning up broken card from {file_path}")
            else:
                cleaned_existing_data.append(card)
        existing_data = cleaned_existing_data
        
        existing_texts = {card["text"].strip() for card in existing_data}
        
        added_count = 0
        for card in rendered_list:
            if card["text"].strip() not in existing_texts:
                existing_data.append(card)
                added_count += 1
                
        save_json(file_path, existing_data)
        print(f"File: {file_path} -> Appended {added_count} pronunciation drill cards. Total: {len(existing_data)}")
        
    # Rebuild index.json
    rebuild_index()

if __name__ == "__main__":
    run()
