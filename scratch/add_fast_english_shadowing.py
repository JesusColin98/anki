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
TARGET_FILE = DECKS_DIR / "03_Languages" / "English" / "Phonetics" / "Connected_Speech.json"

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

# ----------------- Cards Definition -----------------

new_cards = [
    # 1. Stress-Timed Rhythm (T1_Cloze)
    {
        "template": "T1_Cloze",
        "data": {
            "deck": "03_Languages::English::Phonetics::Connected_Speech",
            "scenario": "Fast English: Rhythm & Isocronía ⏳",
            "text": "Unlike syllable-timed languages like Spanish, English is a {{c1::stress-timed language (isocronía)}}, meaning the duration between stressed syllables remains constant, while unstressed syllables are compressed.",
            "explanation": "This means that 'CATS CHASE MICE' and 'The CATS have been CHASING the MICE' take roughly the same amount of time to say. Unstressed words like 'have been' or 'the' are squeezed into tiny fractions of a second, forcing reductions like the schwa.",
            "usage": "Contrast: <code>CATS CHASE MICE</code> (~1.5s) vs. <code>The CATS have been CHASING the MICE</code> (~1.5s).",
            "spanish": "A diferencia de los idiomas con ritmo silábico (como el español), el inglés es un idioma con ritmo acentual (isocronía), lo que significa que el tiempo entre sílabas acentuadas es constante y las sílabas átonas se comprimen."
        }
    },
    # 2. General American Accent (T1_Cloze)
    {
        "template": "T1_Cloze",
        "data": {
            "deck": "03_Languages::English::Phonetics::Connected_Speech",
            "scenario": "Regional Accent: General American (GenAm) 🇺🇸",
            "text": "The General American (GenAm) accent is characterized by full rhoticity, extensive use of {{c1::Flap T and Flap D}} between vowels, and the dropping of /t/ after /n/ in unstressed syllables.",
            "explanation": "Rhoticity means 'r' is pronounced everywhere it is written (e.g. 'car' /kɑːr/). Flapping turns intervocalic /t/ and /d/ into [ɾ], making 'latter' and 'ladder' homophones. Nasal T-deletion turns 'internet' to 'innernet'.",
            "usage": "GenAm features: <code>internet</code> &rarr; 'innernet' | <code>better</code> &rarr; 'bed-er' | <code>water</code> &rarr; 'wa-der'.",
            "spanish": "El acento americano general se caracteriza por su roticidad completa, el uso de la T y D suaves (flaps) entre vocales, y la caída de la T después de la N en sílabas átonas."
        }
    },
    # 3. British RP / Cockney Accents (T1_Cloze)
    {
        "template": "T1_Cloze",
        "data": {
            "deck": "03_Languages::English::Phonetics::Connected_Speech",
            "scenario": "Regional Accent: British RP & Cockney 🇬🇧",
            "text": "The British RP and Cockney accents are non-rhotic and feature prominent {{c1::glottal stops [ʔ]}} in place of intervocalic or final /t/ (e.g. 'bottle' &rarr; 'bo'el'), along with intrusive /r/ linking.",
            "explanation": "Non-rhotic means 'r' is silent unless followed by a vowel. Glottal stop [ʔ] replaces /t/ by closing the vocal folds briefly in the throat. Intrusive R bridges vowel-to-vowel gaps (e.g. 'law and order' &rarr; 'law-r-and-order').",
            "usage": "British features: <code>bottle</code> &rarr; 'bo'el' | <code>law and order</code> &rarr; 'law-r-and-order' | <code>idea of it</code> &rarr; 'idea-r-of-it'.",
            "spanish": "Los acentos británicos RP y Cockney no son róticos, presentan abundante oclusión glotal en lugar de la T intermedia o final, e insertan una R intrusiva de enlace."
        }
    },
    # 4. Southern US & AAVE Accents (T1_Cloze)
    {
        "template": "T1_Cloze",
        "data": {
            "deck": "03_Languages::English::Phonetics::Connected_Speech",
            "scenario": "Regional Accent: Southern US & AAVE 🤠",
            "text": "Southern US English and AAVE (African American Vernacular English) often feature {{c1::monophthongization}} of /aɪ/ (e.g. 'my' &rarr; 'mah'), G-dropping, and final consonant cluster reduction (e.g. 'cold' &rarr; 'cole').",
            "explanation": "Monophthongization turns a two-part vowel glide (diphthong) into a single long vowel. Consonant cluster reduction drops the final stop consonant when sandwiched at the end of words.",
            "usage": "Dialect examples: <code>my friend</code> &rarr; 'mah friend' | <code>cold night</code> &rarr; 'cole night' | <code>running</code> &rarr; 'runnin'' | <code>fixing to</code> &rarr; 'finna'.",
            "spanish": "El inglés del sur de EE. UU. y el AAVE suelen presentar monoptongación (reducción de diptongos a una sola vocal larga, como 'my' &rarr; 'mah'), omisión de G final, y reducción de grupos consonánticos finales ('cold' &rarr; 'cole')."
        }
    },
    # 5. Australian English Accent (T1_Cloze)
    {
        "template": "T1_Cloze",
        "data": {
            "deck": "03_Languages::English::Phonetics::Connected_Speech",
            "scenario": "Regional Accent: Australian English 🇦🇺",
            "text": "Australian English is non-rhotic, features extensive Flap T usage, and is famous for a vowel shift where the diphthong /eɪ/ sounds closer to {{c1::/aɪ/ (like the 'i' in 'bite')}}.",
            "explanation": "Australian vowels are shifted; for example, 'today' sounds similar to 'to-die' to American ears. It also relies heavily on colloquial abbreviations ending in '-ie' or '-o' (e.g. 'breakfast' &rarr; 'brekkie', 'service station' &rarr; 'servo').",
            "usage": "Aussie features: <code>today</code> &rarr; 'to-die' | <code>breakfast</code> &rarr; 'brekkie' | <code>service station</code> &rarr; 'servo'.",
            "spanish": "El inglés australiano no es rótico, usa flaps frecuentes y presenta un cambio vocálico donde el diptongo /eɪ/ se acerca a /aɪ/ ('today' suena similar a 'to-die'), además de abundantes abreviaciones coloquiales."
        }
    },
    # 6. Daily Auditory Decoding Routine (T1_Cloze)
    {
        "template": "T1_Cloze",
        "data": {
            "deck": "03_Languages::English::Phonetics::Connected_Speech",
            "scenario": "Fast English: Auditory Decoding Routine 🎧",
            "text": "The daily 15-minute auditory decoding routine consists of: 5 mins of active phonetic transcription, 5 mins of {{c1::comparison with subtitles & identifying patterns}}, and 5 mins of shadowing (3x repetitions).",
            "explanation": "This routine trains the brain to bridge the gap between spelling and native fast pronunciation. Regular transcription exercises target the 'Jungle Stage' of listening.",
            "usage": "Daily Protocol: <ul><li>Min 0-5: Active transcription (write down what you hear phonetically)</li><li>Min 5-10: Analyze patterns (compare with actual subtitles)</li><li>Min 10-15: Shadowing (repeat 3x trying to mimic speed)</li></ul>",
            "spanish": "La rutina diaria de 15 minutos para decodificación auditiva consiste en: 5 min de transcripción fonética activa, 5 min de cotejo e identificación de patrones, y 5 min de shadowing (repitiendo 3 veces)."
        }
    },
    # 7. Shadowing Drill 1 (T7_Pronunciation)
    {
        "template": "T7_Pronunciation",
        "data": {
            "deck": "03_Languages::English::Phonetics::Connected_Speech",
            "rule_name": "Shadowing: Cluster Elision",
            "formal_phrase": "I must go to the last station. (Challenge: The next-door neighbor said it must be last night.)",
            "fast_pronunciation": "I mus-go to the las-station. (Challenge: The nex-door neighbor said it mus-be las-night.)",
            "explanation": "Cluster Elision (Rule of 3 Consonants): When 3 consonants meet, the middle /t/ or /d/ is dropped.<br>🎥 Search: 'English with Martin Blacutt regla de 3 consonantes elision' on YouTube.<br>🔗 YouGlish search terms: <code>last night</code> / <code>next door</code>",
            "spanish": "Lento: I must go to the last station. Conectado: I mus-go to the las-station. Reto: El vecino de al lado dijo que debió ser anoche."
        }
    },
    # 8. Shadowing Drill 2 (T7_Pronunciation)
    {
        "template": "T7_Pronunciation",
        "data": {
            "deck": "03_Languages::English::Phonetics::Connected_Speech",
            "rule_name": "Shadowing: Flap T / Flap D",
            "formal_phrase": "Put it in a bottle of water while riding the ladder. (Challenge: What a better city to get a job.)",
            "fast_pronunciation": "Pu-di-tin a bo-dle of wa-der while ri-ding the la-der. (Challenge: What a be-rer ci-dy to ge-da job.)",
            "explanation": "Flap T & D (Intervocalic Flapping): Intervocalic /t/ and /d/ turn into soft flap [ɾ].<br>🎥 Search: 'Rachel's English - How to pronounce Flap T' on YouTube.<br>🔗 YouGlish search terms: <code>put it on</code> / <code>better water</code>",
            "spanish": "Lento: Ponlo en una botella de agua mientras montas la escalera. Reto: Qué mejor ciudad para conseguir un trabajo."
        }
    },
    # 9. Shadowing Drill 3 (T7_Pronunciation)
    {
        "template": "T7_Pronunciation",
        "data": {
            "deck": "03_Languages::English::Phonetics::Connected_Speech",
            "rule_name": "Shadowing: Yod Coalescence",
            "formal_phrase": "Don't you know what would you do if I asked you? (Challenge: Did you see what caught you off guard?)",
            "fast_pronunciation": "Don-choo know what wood-joo do if I ask-shoo? (Challenge: Did-joo see what caught-choo off guard?)",
            "explanation": "Yod Coalescence: Merging /t, d, s, z/ with palatal /j/ creates CH, DJ, SH, ZH.<br>🎥 Search: 'BBC Learning English - Tim's Pronunciation Workshop: Assimilation' on YouTube.<br>🔗 YouGlish search terms: <code>don't you</code> / <code>would you</code>",
            "spanish": "Lento: ¿No sabes qué harías si te lo pidiera? Reto: ¿Viste qué te tomó por sorpresa?"
        }
    },
    # 10. Shadowing Drill 4 (T7_Pronunciation)
    {
        "template": "T7_Pronunciation",
        "data": {
            "deck": "03_Languages::English::Phonetics::Connected_Speech",
            "rule_name": "Shadowing: Dark L Vocalization",
            "formal_phrase": "I feel that the milk in the bottle is cold.",
            "fast_pronunciation": "I feew that the miwk in the boddle is cowd.",
            "explanation": "Dark L Vocalization: The back-of-the-mouth L [ɫ] vocalizes to [w] or [ʊ] before consonants or final pauses.<br>🎥 Search: 'Rachel's English Dark L sound' on YouTube.<br>🔗 YouGlish search terms: <code>feel cold</code> / <code>milk bottle</code>",
            "spanish": "Lento: Siento que la leche en la botella está fría. Conectado: I feew that the miwk in the boddle is cowd."
        }
    },
    # 11. Shadowing Drill 5 (T7_Pronunciation)
    {
        "template": "T7_Pronunciation",
        "data": {
            "deck": "03_Languages::English::Phonetics::Connected_Speech",
            "rule_name": "Shadowing: Intrusive Glides",
            "formal_phrase": "Go out and do it because I am ready.",
            "fast_pronunciation": "Go-w-out and do-w-it because I-y-am ready.",
            "explanation": "Intrusive Glides: Inserting linking /w/ or /j/ ('y') to smooth out adjacent vowel clashes.<br>🎥 Search: 'Linking vowels with W and Y sound English' on YouTube.<br>🔗 YouGlish search terms: <code>go out</code> / <code>do it</code>",
            "spanish": "Lento: Sal y hazlo porque estoy listo. Conectado: Go-w-out and do-w-it because I-y-am ready."
        }
    },
    # 12. Shadowing Drill 6 (T7_Pronunciation)
    {
        "template": "T7_Pronunciation",
        "data": {
            "deck": "03_Languages::English::Phonetics::Connected_Speech",
            "rule_name": "Shadowing: Auxiliary Chunks",
            "formal_phrase": "What did you do? Did you ever think it would have been easy? (Challenge: What do you mean how's it going?)",
            "fast_pronunciation": "Whadja do? Jever think it woulda bin easy? (Challenge: Whadaya mean howzit goin'?)",
            "explanation": "Complex Auxiliary Contractions: Compression of auxiliary groups and questions.<br>🎥 Search: 'English reductions whadja jever whadaya' on YouTube.<br>🔗 YouGlish search terms: <code>what did you do</code> / <code>would have been</code>",
            "spanish": "Lento: ¿Qué hiciste? ¿Pensaste que habría sido fácil? Reto: ¿A qué te refieres con cómo te va?"
        }
    }
]

def run():
    print("=== GENERATING FAST ENGLISH SHADOWING & ACCENT CARDS ===")
    
    existing_cards = load_json(TARGET_FILE)
    existing_texts = {card["text"].strip() for card in existing_cards}
    
    added_count = 0
    for card_def in new_cards:
        # Build card using template engine
        rendered = build_card(card_def["template"], card_def["data"])
        
        if rendered["text"].strip() not in existing_texts:
            existing_cards.append(rendered)
            added_count += 1
            
    save_json(TARGET_FILE, existing_cards)
    print(f"File: {TARGET_FILE} -> Appended {added_count} new cards. Total cards: {len(existing_cards)}")
    
    # Rebuild index
    rebuild_index()

if __name__ == "__main__":
    run()
