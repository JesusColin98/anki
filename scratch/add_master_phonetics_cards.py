import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DECKS_DIR = BASE_DIR / "decks"

def load_or_create_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {file_path}. Initializing empty list.")
                return []
    else:
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        return []

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {file_path} (Total cards: {len(data)})")

def rebuild_index():
    index_path = DECKS_DIR / "index.json"
    decks_list = []
    total_cards = 0
    
    # Recurse through DECKS_DIR
    for root, _, files in os.walk(DECKS_DIR):
        for file in sorted(files):
            if file.endswith(".json") and file != "index.json":
                file_path = Path(root) / file
                rel_path = os.path.relpath(file_path, DECKS_DIR)
                # Standard deck name derivation from path
                derived_deck = str(Path(rel_path).with_suffix("")).replace(os.sep, "::")
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        cards = json.load(f)
                    
                    # Store deck metadata
                    decks_list.append({
                        "deck": derived_deck,
                        "path": f"decks/{rel_path.replace(os.sep, '/')}",
                        "cards_count": len(cards)
                    })
                    total_cards += len(cards)
                except Exception as e:
                    print(f"Error reading {file_path} for index rebuild: {e}")
                    
    # Sort decks alphabetically
    decks_list.sort(key=lambda x: x["deck"])
    
    index_data = {
        "total_cards": total_cards,
        "total_decks": len(decks_list),
        "decks": decks_list
    }
    
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    print(f"\nRebuilt index: {index_path} with {len(decks_list)} decks and {total_cards} total cards.")

# ----------------- Cards definition -----------------

# 1. Fast English (Connected Speech) - 8 Cards
english_cards = [
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Nasal T-Deletion 👃",
        "text": "In American English, a /t/ following a /n/ in an unstressed syllable is often {{c1::omitted (dropped)}}, making \"twenty\" sound like \"tweny\" and \"internet\" sound like \"innernet\".",
        "explanation": "Because /n/ and /t/ are both pronounced at the alveolar ridge, and /n/ is nasalized, the nasal airflow dominates when the syllable is unstressed, leading the speaker to skip the stop /t/ completely.",
        "usage": "Practice Drills:<ul><li><code>twenty</code> &rarr; \"tweny\"</li><li><code>internet</code> &rarr; \"innernet\"</li><li><code>center</code> &rarr; \"cener\"</li><li><code>international</code> &rarr; \"innernational\"</li></ul>",
        "spanish": "En inglés americano, la /t/ después de una /n/ en una sílaba átona a menudo se omite. Ejemplo: \"twenty\" suena como \"tweny\" e \"internet\" como \"innernet\".",
        "tags": ["english", "phonetics", "connected_speech", "t_deletion"]
    },
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Linking & Intrusive R 🔗",
        "text": "In non-rhotic accents (e.g., British RP), speakers insert a {{c1::Linking or Intrusive R}} between two words when the first ends in a vowel and the second starts with a vowel, as in \"law and order\" sounding like \"law-r-and-order\".",
        "explanation": "Non-rhotic speakers do not pronounce 'r' at the end of words (e.g., 'car' is /kɑː/). However, if the next word starts with a vowel, they activate it as a 'Linking R' (e.g., 'car is' &rarr; /kɑːr ɪz/). If there is no 'r' in the spelling but the vowels clash, they insert an 'Intrusive R' (e.g., 'idea of' &rarr; /aɪˈdɪə.rəv/).",
        "usage": "Practice Drills:<ul><li><code>law and order</code> &rarr; \"law-r-an-order\"</li><li><code>idea of it</code> &rarr; \"idea-r-of-it\"</li><li><code>media event</code> &rarr; \"media-r-event\"</li></ul>",
        "spanish": "En acentos no róticos (como el británico RP), los hablantes insertan una R de enlace ('Linking/Intrusive R') entre palabras cuando una termina en vocal y la otra empieza en vocal. Ejemplo: \"law and order\" &rarr; \"law-r-and-order\".",
        "tags": ["english", "phonetics", "connected_speech", "linking_r", "intrusive_r"]
    },
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Lexical Compressions (Chunking) 🗣️",
        "text": "Highly frequent word combinations are compressed into single colloquial units: \"going to\" becomes {{c1::gonna}}, \"want to\" becomes {{c2::wanna}}, and \"don't know\" becomes {{c3::dunno}}.",
        "explanation": "Lexical chunking occurs because these high-frequency phrases are retrieved as a single cognitive unit, allowing the articulatory organs to take extreme shortcuts.",
        "usage": "Practice Drills:<ul><li><code>going to go</code> &rarr; \"gonna go\"</li><li><code>want to eat</code> &rarr; \"wanna eat\"</li><li><code>I don't know</code> &rarr; \"I dunno\"</li><li><code>got to leave</code> &rarr; \"gotta leave\"</li></ul>",
        "spanish": "Combinaciones de palabras muy frecuentes se comprimen en unidades coloquiales: \"going to\" se convierte en \"gonna\", \"want to\" en \"wanna\", y \"don't know\" en \"dunno\".",
        "tags": ["english", "phonetics", "connected_speech", "chunking", "reductions"]
    },
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Unreleased Stops 🤐",
        "text": "When a stop consonant (/p, t, k, b, d, g/) occurs at the end of a word or before another consonant, native speakers often use an {{c1::unreleased stop [̚]}}, meaning they block the air without letting it explode out.",
        "explanation": "Instead of releasing the air pressure with a small burst of air (as in citation form), the airflow is stopped by the tongue or lips and held, resulting in an abrupt cut-off of the preceding vowel.",
        "usage": "Practice Drills:<ul><li><code>stop it</code> &rarr; \"stop-it\" (held lip closure)</li><li><code>hot dog</code> &rarr; \"hot-dog\" (tongue stays on alveolar ridge)</li><li><code>cat food</code> &rarr; \"cat-food\" (abrupt stop before 'f')</li></ul>",
        "spanish": "Cuando una consonante oclusiva (/p, t, k, b, d, g/) está al final de una palabra o antes de otra consonante, se suele retener la liberación de aire (oclusión retenida), cortando el sonido de golpe.",
        "tags": ["english", "phonetics", "connected_speech", "stops", "unreleased"]
    },
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Flap D ⚡",
        "text": "In American English, a /d/ between vowels behaves exactly like a /t/, turning into a {{c1::Flap D [ɾ]}} (which sounds identical to a Flap T), making \"ladder\" homophonous with \"latter\".",
        "explanation": "Because the tongue tap is so fast, the distinction between the voiced /d/ and voiceless /t/ is neutralized in this position, resulting in the same alveolar flap [ɾ] sound.",
        "usage": "Contrastive Pairs (Sound Identical):<ul><li><code>ladder</code> vs. <code>latter</code> (/ˈlæ.ɾər/)</li><li><code>riding</code> vs. <code>writing</code> (/ˈraɪ.ɾɪŋ/)</li><li><code>beading</code> vs. <code>beating</code> (/ˈbiː.ɾɪŋ/)</li></ul>",
        "spanish": "En inglés americano, la /d/ entre vocales se convierte en una 'Flap D' [ɾ] (idéntica a la Flap T), haciendo que palabras como \"ladder\" (escalera) y \"latter\" (último) suenen igual.",
        "tags": ["english", "phonetics", "connected_speech", "flap_d", "homophones"]
    },
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Pre-Glottalization 🤐",
        "text": "Before voiceless stops (/p, t, k/) at the end of syllables, speakers often reinforce the consonant with a simultaneous closing of the vocal cords, a process called {{c1::Pre-Glottalization or Glottal Reinforcement}}.",
        "explanation": "The glottis closes briefly just before or during the oral closure for the stop consonant. This makes the onset of the consonant sound sharper and prevents voicing.",
        "usage": "Practice Drills:<ul><li><code>napkin</code> &rarr; \"na[ʔ]pkin\"</li><li><code>actor</code> &rarr; \"a[ʔ]ctor\"</li><li><code>backward</code> &rarr; \"ba[ʔ]kward\"</li></ul>",
        "spanish": "Antes de las consonantes sordas /p, t, k/ al final de una sílaba, los hablantes a menudo cierran las cuerdas vocales simultáneamente, reforzando el sonido (pre-glotalización).",
        "tags": ["english", "phonetics", "connected_speech", "glottalization", "stops"]
    },
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Advanced Auxiliary Chunks 🗣️",
        "text": "Complex auxiliary verb structures are heavily contracted in native conversation: \"What did you do?\" becomes {{c1::\"whadja do?\"}} and \"would have been\" becomes {{c2::\"woulda bin\"}}.",
        "explanation": "Auxiliary and modal verbs carry low semantic weight compared to main verbs and nouns. In rapid speech, they undergo extreme vowel reduction and coalescence to speed up delivery.",
        "usage": "Practice Drills:<ul><li><code>What did you do?</code> &rarr; \"whadja do?\"</li><li><code>Did you ever...?</code> &rarr; \"jever...?\"</li><li><code>would have been</code> &rarr; \"woulda bin\"</li><li><code>What do you mean?</code> &rarr; \"whadaya mean?\"</li></ul>",
        "spanish": "Las estructuras de verbos auxiliares complejos se contraen de forma extrema: \"What did you do?\" se convierte en \"whadja do?\" y \"would have been\" en \"woulda bin\".",
        "tags": ["english", "phonetics", "connected_speech", "auxiliary", "reductions"]
    },
    {
        "deck": "03_Languages::English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Syllabic Consonants 🗣️",
        "text": "When an unstressed vowel is followed by /l/, /n/, or /m/, the vowel is often dropped completely, and the consonant itself becomes the nucleus of the syllable, known as a {{c1::Syllabic Consonant [n̩, l̩, m̩]}} (e.g., \"button\" &rarr; /ˈbʌ.tn̩/).",
        "explanation": "Instead of pronouncing the schwa /ə/ and then the consonant, the tongue transitions directly from the preceding consonant to the nasal/lateral position, eliminating the vowel sound entirely.",
        "usage": "Practice Drills:<ul><li><code>button</code> &rarr; \"butt-n\" (/ˈbʌ.tn̩/)</li><li><code>little</code> &rarr; \"litt-l\" (/ˈlɪ.tl̩/)</li><li><code>rhythm</code> &rarr; \"rhyth-m\" (/ˈrɪð.m̩/)</li><li><code>sudden</code> &rarr; \"sudd-n\" (/ˈsʌd.n̩/)</li></ul>",
        "spanish": "Cuando una vocal átona es seguida por /l/, /n/ o /m/, la vocal se elimina y la consonante actúa como núcleo de la sílaba (consonante silábica). Ejemplo: \"button\" suena como \"butt-n\".",
        "tags": ["english", "phonetics", "connected_speech", "syllabic_consonants"]
    }
]

# 2. Spanish - 4 Cards
spanish_cards = [
    {
        "deck": "03_Languages::Spanish::Phonetics::General",
        "scenario": "Spanish Phonetics 🗣️",
        "text": "In Spanish phonetics, the rule of {{c1::Sinalefa (Vowel Merging)}} is defined as: Contiguous vowels between words merge into a single syllable in fast speech (e.g., *de una vez* &rarr; [djuna.βes]).",
        "explanation": "Spanish speakers seek vocal continuity. Instead of pausing between word boundaries, contiguous vowels flow into a single syllable, creating a smooth stream of speech.",
        "usage": "Rule: <code>Sinalefa</code><br>Examples:<ul><li><code>La amiga</code> &rarr; \"Lamiga\"</li><li><code>Mi hijo</code> &rarr; \"Mijo\"</li><li><code>De una vez</code> &rarr; \"Duna vez\"</li></ul>",
        "spanish": "Sinalefa: Unión de vocales contiguas de palabras distintas en una sola sílaba métrica/rítmica. Ejemplo: \"de una vez\" &rarr; [djuna.βes].",
        "tags": ["languages_path", "spanish", "phonetics", "connected_speech", "sinalefa"]
    },
    {
        "deck": "03_Languages::Spanish::Phonetics::General",
        "scenario": "Spanish Phonetics 🗣️",
        "text": "In Spanish phonetics, the rule of {{c1::Aspiración / Elisión de 'S'}} is defined as: In fast speech (particularly in Caribbean and Southern dialects), syllable-final /s/ is aspirated to [h] or dropped entirely (e.g., *los mismos* &rarr; [lo.mih.moh] or [lo.mi.mo]).",
        "explanation": "The drop or aspiration of the sibilant 's' in codas is a key phonetic marker of coastal Spanish dialects, occurring to optimize articulatory speed.",
        "usage": "Rule: <code>Aspiración / Elisión de 'S'</code><br>Examples:<ul><li><code>los mismos</code> &rarr; \"lo' mi'mo'\"</li><li><code>estás listo</code> &rarr; \"ehta' liht-o\"</li></ul>",
        "spanish": "Aspiración / Elisión de 'S' final: Reducción de la /s/ al final de sílaba a un soplo aspirado [h] o desaparición total. Ejemplo: \"los mismos\" &rarr; \"lo' mi'mo'\".",
        "tags": ["languages_path", "spanish", "phonetics", "connected_speech", "s_elision"]
    },
    {
        "deck": "03_Languages::Spanish::Phonetics::General",
        "scenario": "Spanish Phonetics 🗣️",
        "text": "In Spanish phonetics, the rule of {{c1::Intervocalic 'D' Weakening}} is defined as: The sound /d/ between vowels is weakened or dropped entirely in colloquial fast speech (e.g., *cansado* &rarr; [kanˈsao], *para nada* &rarr; [pa.na]).",
        "explanation": "Because /d/ is a soft dental approximant [ð] between vowels, articulatory laziness leads speakers to drop the tongue contact completely, converting it into a vowel glide.",
        "usage": "Rule: <code>Intervocalic 'D' Weakening</code><br>Examples:<ul><li><code>cansado</code> &rarr; \"cansao\"</li><li><code>para nada</code> &rarr; \"pa' na'\"</li><li><code>todo el día</code> &rarr; \"to'el día\"</li></ul>",
        "spanish": "Debilitamiento de la 'D' intervocálica: Caída o relajación extrema del fonema dental /d/ entre vocales. Ejemplo: \"cansado\" &rarr; \"cansao\".",
        "tags": ["languages_path", "spanish", "phonetics", "connected_speech", "d_weakening"]
    },
    {
        "deck": "03_Languages::Spanish::Phonetics::General",
        "scenario": "Spanish Phonetics 🗣️",
        "text": "In Spanish phonetics, the rule of {{c1::N-M Assimilation}} is defined as: The nasal /n/ before a bilabial consonant (/p, b, m/) assimilates to a bilabial [m] (e.g., *un beso* &rarr; [um.ˈbe.so]).",
        "explanation": "To prepare the mouth for the upcoming bilabial sound, the tongue skips the alveolar contact for /n/ and uses lip-closure directly.",
        "usage": "Rule: <code>N-M Assimilation</code><br>Examples:<ul><li><code>un beso</code> &rarr; \"um beso\"</li><li><code>sin pensar</code> &rarr; \"sim pensar\"</li><li><code>en mi casa</code> &rarr; \"em mi casa\"</li></ul>",
        "spanish": "Asimilación N-M: La consonante alveolar nasal /n/ se convierte en bilabial [m] antes de /p, b, m/. Ejemplo: \"un beso\" &rarr; [um.ˈbe.so].",
        "tags": ["languages_path", "spanish", "phonetics", "connected_speech", "assimilation"]
    }
]

# 3. Chinese - 3 Cards
chinese_cards = [
    {
        "deck": "03_Languages::Chinese::Phonetics::General",
        "scenario": "Chinese Phonetics 🗣️",
        "text": "In Mandarin Chinese phonetics, the rule of {{c1::Erhua (儿化)}} is defined as: A suffix '-r' is added to the end of a syllable, causing the vowel to blend with a retroflex /r/ sound (e.g., *Zhe er* 这儿 &rarr; \"Zher\").",
        "explanation": "Highly characteristic of Beijing and northern dialects, Erhua merges the noun suffix 'er' (child) with the preceding syllable, causing vowel reduction or retroflex coloring.",
        "usage": "Rule: <code>Erhua (儿化)</code><br>Examples:<ul><li><code>Zhe er (这儿)</code> &rarr; \"Zher\"</li><li><code>Wan er (玩儿)</code> &rarr; \"Waer\"</li><li><code>Yi dian er (一点儿)</code> &rarr; \"Yidianr\"</li></ul>",
        "spanish": "Erhua (儿化): Fusión de la 'R' al final de la sílaba engullendo o modificando la vocal. Ejemplo: \"Zhe er\" &rarr; \"Zher\".",
        "tags": ["languages_path", "chinese", "phonetics", "connected_speech", "erhua"]
    },
    {
        "deck": "03_Languages::Chinese::Phonetics::General",
        "scenario": "Chinese Phonetics 🗣️",
        "text": "In Mandarin Chinese phonetics, the rule of {{c1::Neutral Tone (轻声)}} is defined as: Unstressed syllables lose their original tone and are pronounced short and soft (e.g., *Shi shen me* 什么 &rarr; \"Shenme\").",
        "explanation": "Functional particles (like de, ma) and the second character in many compound nouns lose their tone in fast speech, taking on a pitch determined by the preceding syllable.",
        "usage": "Rule: <code>Neutral Tone (轻声)</code><br>Examples:<ul><li><code>Baba (爸爸)</code> &rarr; High-falling followed by short/neutral</li><li><code>Shenme (什么)</code> &rarr; \"Shenme\" (unstressed second syllable)</li></ul>",
        "spanish": "Tono Neutro (轻声): Pérdida del tono original en sílabas secundarias, pronunciadas de forma corta y suave.",
        "tags": ["languages_path", "chinese", "phonetics", "connected_speech", "neutral_tone"]
    },
    {
        "deck": "03_Languages::Chinese::Phonetics::General",
        "scenario": "Chinese Phonetics 🗣️",
        "text": "In Mandarin Chinese phonetics, the rule of {{c1::Syllable Contraction}} is defined as: High-frequency adjacent syllables contract by dropping vowels or initials (e.g., *Bu yong* 不用 &rarr; \"Bong\", *Bu zhi dao* 不知道 &rarr; \"Buzdao\").",
        "explanation": "Common conversational expressions contract in fast speech by blending the initial of the first syllable with the final of the second.",
        "usage": "Rule: <code>Syllable Contraction</code><br>Examples:<ul><li><code>Bu yong (不用)</code> &rarr; \"Bong\"</li><li><code>Bu zhi dao (不知道)</code> &rarr; \"Buzdao\"</li><li><code>Shenme (什么)</code> &rarr; \"Shem\"</li></ul>",
        "spanish": "Contracción Silábica: Fusión de dos sílabas frecuentes en un solo sonido comprimido. Ejemplo: \"Bu yong\" &rarr; \"Bong\".",
        "tags": ["languages_path", "chinese", "phonetics", "connected_speech", "contraction"]
    }
]

# 4. French - 3 Cards
french_cards = [
    {
        "deck": "03_Languages::French::Phonetics::General",
        "scenario": "French Phonetics 🗣️",
        "text": "In French phonetics, the rule of {{c1::La Liaison}} is defined as: A normally silent final consonant is pronounced and linked to the initial vowel of the following word (e.g., *les enfants* &rarr; /le.zɑ̃.fɑ̃/).",
        "explanation": "Liaison maintains phonetic flow (enchaînement) by avoiding hiatus (the clashing of two vowels). The silent consonant is resurrected to serve as the onset of the next word's syllable.",
        "usage": "Rule: <code>La Liaison</code><br>Examples:<ul><li><code>les enfants</code> &rarr; \"le-zanfan\"</li><li><code>vous avez</code> &rarr; \"vou-zavez\"</li><li><code>un petit ami</code> &rarr; \"un peti-tami\"</li></ul>",
        "spanish": "La Liaison: Pronunciación de una consonante final muda al unirse con una palabra que empieza por vocal. Ejemplo: \"les enfants\" &rarr; \"le-zanfan\".",
        "tags": ["languages_path", "french", "phonetics", "connected_speech", "liaison"]
    },
    {
        "deck": "03_Languages::French::Phonetics::General",
        "scenario": "French Phonetics 🗣️",
        "text": "In French phonetics, the rule of {{c1::Elision of 'E' Muet (Schwa Deletion)}} is defined as: Unstressed mute 'e' is dropped in fast speech, merging consonants (e.g., *je ne sais pas* &rarr; \"j'sais pas\" /ʃe.pa/).",
        "explanation": "Dropping the schwa /ə/ (e caduc) is the most prominent feature of rapid spoken French, reducing the syllable count and leading to consonant voicing assimilation (e.g., /ʒ/ becomes voiceless /ʃ/ before /s/).",
        "usage": "Rule: <code>Elision of 'E' Muet</code><br>Examples:<ul><li><code>je ne sais pas</code> &rarr; \"j'sais pas\" (sounds like \"she-pa\")</li><li><code>petit</code> &rarr; \"p'tit\"</li><li><code>tout de suite</code> &rarr; \"tout'suite\"</li></ul>",
        "spanish": "Caída de la 'E' muda: Omisión del sonido schwa francés en el habla rápida, provocando asimilación de consonantes contiguas.",
        "tags": ["languages_path", "french", "phonetics", "connected_speech", "schwa_elision"]
    },
    {
        "deck": "03_Languages::French::Phonetics::General",
        "scenario": "French Phonetics 🗣️",
        "text": "In French phonetics, the rule of {{c1::Pronoun Compression}} is defined as: Pronoun groups contract by elision of vowels and merging of syllables in rapid speech (e.g., *il y a* &rarr; \"y'a\" /ja/, *tu as* &rarr; \"t'as\").",
        "explanation": "Subject and object pronouns before verbs are unstressed functional elements and undergo severe contraction in native conversational speed.",
        "usage": "Rule: <code>Pronoun Compression</code><br>Examples:<ul><li><code>il y a</code> &rarr; \"y'a\"</li><li><code>tu as</code> &rarr; \"t'as\"</li><li><code>je suis</code> &rarr; \"chuis\" (/ʃɥi/)</li></ul>",
        "spanish": "Compresión de Pronombres: Contracción y elisión de vocales en grupos de pronombres rápidos. Ejemplo: \"il y a\" &rarr; \"y'a\".",
        "tags": ["languages_path", "french", "phonetics", "connected_speech", "pronoun_compression"]
    }
]

# 5. German - 3 Cards
german_cards = [
    {
        "deck": "03_Languages::German::Phonetics::General",
        "scenario": "German Phonetics 🗣️",
        "text": "In German phonetics, the rule of {{c1::Auslautverhärtung (Final Devoicing)}} is defined as: Voiced stops and fricatives (/b, d, ɡ, v, z/) become voiceless ([p, t, k, f, s]) at the end of a syllable or word (e.g., *Hund* &rarr; [hʊnt], *Tag* &rarr; [taːk]).",
        "explanation": "This phonological rule is absolute in standard German. Even if a word is spelled with a voiced consonant, it is pronounced as its voiceless pair when placed in the syllable coda.",
        "usage": "Rule: <code>Auslautverhärtung</code><br>Examples:<ul><li><code>Hund (dog)</code> &rarr; \"Hunt\"</li><li><code>Tag (day)</code> &rarr; \"Taak\"</li><li><code>aktiv (active)</code> &rarr; ends in \"f\" sound</li></ul>",
        "spanish": "Auslautverhärtung (Dessonorización Final): Ensordecimiento de consonantes sonoras /b, d, g, v, z/ al final de sílaba. Ejemplo: \"Hund\" &rarr; \"Hunt\".",
        "tags": ["languages_path", "german", "phonetics", "connected_speech", "devoicing"]
    },
    {
        "deck": "03_Languages::German::Phonetics::General",
        "scenario": "German Phonetics 🗣️",
        "text": "In German phonetics, the rule of {{c1::Knacklaut (Glottal Stop)}} is defined as: A sharp glottal stop [ʔ] is inserted before words beginning with a stressed vowel, preventing liaison (e.g., *ich esse* &rarr; [ʔɪç ˈʔɛsə]).",
        "explanation": "Unlike English or French where words link seamlessly, German reinforces word boundaries by cutting the airflow in the vocal cords before word-initial vowels, creating a staccato rhythm.",
        "usage": "Rule: <code>Knacklaut (Glottal Stop)</code><br>Examples:<ul><li><code>ich esse</code> &rarr; \"ich [ʔ]esse\" (no liaison)</li><li><code>Verein</code> &rarr; \"Ver-[ʔ]ein\" (internal boundary)</li></ul>",
        "spanish": "Knacklaut (Oclusión Glotal): Oclusión brusca de las cuerdas vocales antes de una vocal inicial acentuada, evitando la ligadura. Ejemplo: \"ich esse\" &rarr; \"ich [ʔ]esse\".",
        "tags": ["languages_path", "german", "phonetics", "connected_speech", "glottal_stop"]
    },
    {
        "deck": "03_Languages::German::Phonetics::General",
        "scenario": "German Phonetics 🗣️",
        "text": "In German phonetics, the rule of {{c1::Reduction of final '-en'}} is defined as: The final unstressed syllable '-en' loses its vowel, making the consonant syllabic or merging with the previous consonant (e.g., *kommen* &rarr; [ˈkɔm.n̩], *haben* &rarr; [ˈhaːb.m̩]).",
        "explanation": "In native speech, the suffix '-en' (representing infinitive/plural endings) reduces the schwa /ə/ completely. The /n/ then becomes syllabic, often assimilating to the place of articulation of the preceding consonant (e.g., bilabial /b/ turns /n/ into /m/).",
        "usage": "Rule: <code>Reduction of final '-en'</code><br>Examples:<ul><li><code>kommen</code> &rarr; \"komm'n\" (/ˈkɔm.n̩/)</li><li><code>haben</code> &rarr; \"hab'm\" (/ˈhaːb.m̩/)</li><li><code>gehen</code> &rarr; \"geh'n\" (/ˈɡeː.n̩/)</li></ul>",
        "spanish": "Reducción de terminación '-en': Elisión de la vocal en la sílaba final '-en', convirtiendo la consonante en silábica o asimilándola. Ejemplo: \"kommen\" &rarr; \"komm'n\".",
        "tags": ["languages_path", "german", "phonetics", "connected_speech", "en_reduction"]
    }
]

# 6. Italian - 2 Cards
italian_cards = [
    {
        "deck": "03_Languages::Italian::Phonetics::General",
        "scenario": "Italian Phonetics 🗣️",
        "text": "In Italian phonetics, the rule of {{c1::Raddoppiamento Fonosintattico}} is defined as: The initial consonant of a word is lengthened (geminated) when preceded by a word ending in a stressed vowel (e.g., *caffè espresso* &rarr; \"caffè m-espresso\", *a casa* &rarr; \"a-ccasa\").",
        "explanation": "Raddoppiamento (syntactic gemination) occurs when the final stressed vowel triggers phonological doubling of the onset consonant of the next word, standardizing speech flow.",
        "usage": "Rule: <code>Raddoppiamento Fonosintattico</code><br>Examples:<ul><li><code>a casa</code> &rarr; \"a ccasa\"</li><li><code>caffè espresso</code> &rarr; \"caffè m-espresso\"</li><li><code>chi sei</code> &rarr; \"chi ssei\"</li></ul>",
        "spanish": "Raddoppiamento Fonosintattico: Duplicación de la consonante inicial de una palabra cuando va precedida de una vocal tónica. Ejemplo: \"a casa\" &rarr; \"a-ccasa\".",
        "tags": ["languages_path", "italian", "phonetics", "connected_speech", "gemination"]
    },
    {
        "deck": "03_Languages::Italian::Phonetics::General",
        "scenario": "Italian Phonetics 🗣️",
        "text": "In Italian phonetics, the rule of {{c1::Troncamento (Apocope)}} is defined as: The dropping of a final vowel or syllable in certain words, especially before words beginning with a consonant (e.g., *un poco* &rarr; \"un po'\", *buono giorno* &rarr; \"buongiorno\").",
        "explanation": "Troncamento speeds up pronunciation by truncating words, creating single lexical units for commonly paired words.",
        "usage": "Rule: <code>Troncamento (Apocope)</code><br>Examples:<ul><li><code>un poco</code> &rarr; \"un po'\"</li><li><code>buono giorno</code> &rarr; \"buongiorno\"</li><li><code>dottore Rossi</code> &rarr; \"dottor Rossi\"</li></ul>",
        "spanish": "Troncamento (Apócope Vocálica): Caída de una vocal o sílaba final en ciertas palabras para agilizar el habla. Ejemplo: \"un poco\" &rarr; \"un po'\".",
        "tags": ["languages_path", "italian", "phonetics", "connected_speech", "apocope"]
    }
]

# 7. Portuguese - 3 Cards
portuguese_cards = [
    {
        "deck": "03_Languages::Portuguese::Phonetics::General",
        "scenario": "Portuguese Phonetics 🗣️",
        "text": "In Portuguese phonetics, the rule of {{c1::Palatalization of T/D (BR)}} is defined as: In Brazilian Portuguese, /t/ and /d/ become affricates [tʃ] and [dʒ] before the vowel /i/ or unstressed /e/ (e.g., *dia* &rarr; [ˈdʒi.ɐ], *tia* &rarr; [ˈtʃi.ɐ]).",
        "explanation": "Palatalization is a defining feature of Brazilian Portuguese (carioca, paulista, etc.), where dental stops become post-alveolar affricates due to vocalic context.",
        "usage": "Rule: <code>Palatalization of T/D (BR)</code><br>Examples:<ul><li><code>dia (day)</code> &rarr; \"djia\"</li><li><code>tia (aunt)</code> &rarr; \"tchia\"</li><li><code>de tarde</code> &rarr; \"dji tardji\"</li></ul>",
        "spanish": "Palatalización de T y D (Brasil): Conversión de las dentales /t/ y /d/ en las africadas \"tch\" /tʃ/ y \"dj\" /dʒ/ antes de la vocal /i/ o /e/ átona. Ejemplo: \"dia\" &rarr; \"djia\".",
        "tags": ["languages_path", "portuguese", "phonetics", "connected_speech", "palatalization"]
    },
    {
        "deck": "03_Languages::Portuguese::Phonetics::General",
        "scenario": "Portuguese Phonetics 🗣️",
        "text": "In Portuguese phonetics, the rule of {{c1::L-Vocalization (BR)}} is defined as: In Brazilian Portuguese, syllable-final /l/ is vocalized to the glide [w] (e.g., *Brasil* &rarr; [bɾaˈziw], *sol* &rarr; [sɔw]).",
        "explanation": "In Brazil, word-final L is vocalized to a semivowel 'w' instead of using a velarized 'dark L' as in Portugal, changing the syllable rhyme.",
        "usage": "Rule: <code>L-Vocalization (BR)</code><br>Examples:<ul><li><code>Brasil</code> &rarr; \"Brasiw\"</li><li><code>sol (sun)</code> &rarr; \"sow\"</li><li><code>papel</code> &rarr; \"papew\"</li></ul>",
        "spanish": "Vocalización de la 'L' final (Brasil): La /l/ al final de sílaba se vocaliza en la semivocal [w]. Ejemplo: \"Brasil\" &rarr; \"Brasiw\".",
        "tags": ["languages_path", "portuguese", "phonetics", "connected_speech", "l_vocalization"]
    },
    {
        "deck": "03_Languages::Portuguese::Phonetics::General",
        "scenario": "Portuguese Phonetics 🗣️",
        "text": "In Portuguese phonetics, the rule of {{c1::Vowel Reduction (PT-PT)}} is defined as: In European Portuguese, unstressed vowels undergo extreme reduction or are deleted entirely, making the language sound stress-timed (e.g., *excelente* &rarr; [ʃs.ˈlẽt]).",
        "explanation": "European Portuguese has a highly stress-timed rhythm characterized by the complete compression of unstressed syllables and loss of vowels, leaving clusters of consonants.",
        "usage": "Rule: <code>Vowel Reduction (PT-PT)</code><br>Examples:<ul><li><code>excelente</code> &rarr; \"shs-lẽt\"</li><li><code>português</code> &rarr; \"prtu-guêsh\"</li></ul>",
        "spanish": "Reducción Vocálica Extrema (Portugal): Reducción o eliminación total de vocales átonas, lo que da un ritmo acompasado por acentos. Ejemplo: \"excelente\" &rarr; [ʃs.ˈlẽt].",
        "tags": ["languages_path", "portuguese", "phonetics", "connected_speech", "vowel_reduction"]
    }
]

# 8. Japanese - 3 Cards
japanese_cards = [
    {
        "deck": "03_Languages::Japanese::Phonetics::General",
        "scenario": "Japanese Phonetics 🗣️",
        "text": "In Japanese phonetics, the rule of {{c1::Vowel Devoicing (無声化)}} is defined as: High vowels /i/ and /u/ lose their voicing between voiceless consonants or at the end of a sentence following a voiceless consonant (e.g., *desu* &rarr; \"des'\", *suki* &rarr; \"s-ki\").",
        "explanation": "Devoicing occurs because the vocal cords do not vibrate during the transition between two voiceless consonants (like /s/ and /k/), silencing the high vowels.",
        "usage": "Rule: <code>Vowel Devoicing (無声化)</code><br>Examples:<ul><li><code>desu (to be)</code> &rarr; \"des'\"</li><li><code>suki (like)</code> &rarr; \"s-ki\"</li><li><code>shita (under)</code> &rarr; \"sh-ta\"</li></ul>",
        "spanish": "Dessonorización de Vocales 'U' e 'I': Las vocales altas pierden su sonoridad cuando están entre consonantes sordas o al final de frase tras consonante sorda. Ejemplo: \"desu\" &rarr; \"des'\".",
        "tags": ["languages_path", "japanese", "phonetics", "connected_speech", "devoicing"]
    },
    {
        "deck": "03_Languages::Japanese::Phonetics::General",
        "scenario": "Japanese Phonetics 🗣️",
        "text": "In Japanese phonetics, the rule of {{c1::Sokuon (促音)}} is defined as: The small *tsu* (っ) represents a double consonant, causing a one-mora pause (air blockage) before pronouncing the next sorda consonant (e.g., *matte* &rarr; [maʔte]).",
        "explanation": "The Sokuon represents a geminate consonant that takes exactly one mora (unit of time) of silence, during which the mouth prepares the shape for the next consonant.",
        "usage": "Rule: <code>Sokuon (促音)</code><br>Examples:<ul><li><code>matte (wait)</code> &rarr; \"ma [pause] te\"</li><li><code>gakkou (school)</code> &rarr; \"ga [pause] kou\"</li></ul>",
        "spanish": "Sokuon (っ): La pequeña tsu representa una pausa de una mora (detención de aire) antes de una consonante sorda. Ejemplo: \"matte\" &rarr; \"ma-tte\".",
        "tags": ["languages_path", "japanese", "phonetics", "connected_speech", "sokuon"]
    },
    {
        "deck": "03_Languages::Japanese::Phonetics::General",
        "scenario": "Japanese Phonetics 🗣️",
        "text": "In Japanese phonetics, the rule of {{c1::Colloquial Contractions}} is defined as: High-frequency verb endings compress in casual fast speech (e.g., *~te shimau* &rarr; \"~tchau\", *~de wa* &rarr; \"~ja\").",
        "explanation": "Common grammaticized auxiliaries contract heavily in casual speed: the glide /j/ fuses with preceding dental consonants.",
        "usage": "Rule: <code>Colloquial Contractions</code><br>Examples:<ul><li><code>tabete shimau</code> &rarr; \"tabetchau\"</li><li><code>de wa nai</code> &rarr; \"ja nai\"</li><li><code>te oku</code> &rarr; \"toku\"</li></ul>",
        "spanish": "Contracciones Coloquiales: Reducciones extremas de terminaciones de verbos en el habla rápida informal. Ejemplo: \"~te shimau\" &rarr; \"~tchau\".",
        "tags": ["languages_path", "japanese", "phonetics", "connected_speech", "contractions"]
    }
]

# 9. Hindi (New Deck) - 3 Cards
hindi_cards = [
    {
        "deck": "03_Languages::Hindi::Phonetics::General",
        "scenario": "Hindi Phonetics 🗣️",
        "text": "In Hindi phonetics, the rule of {{c1::Schwa Deletion (Syncope)}} is defined as: The inherent schwa vowel /ə/ in consonants is automatically deleted at the end of words or in unstressed intermediate syllables (e.g., *Khabara* खबर &rarr; \"Khabr\").",
        "explanation": "Hindi inherits a silent default schwa vowel in consonants from Sanskrit. In modern fast Hindi, this schwa is dropped in syllable codas, which dictates the correct pronunciation of verb and noun endings.",
        "usage": "Rule: <code>Schwa Deletion</code><br>Examples:<ul><li><code>Khabara (news)</code> &rarr; \"Khabr\"</li><li><code>Karanā (to do)</code> &rarr; \"Karnaa\"</li><li><code>Bharata (India)</code> &rarr; \"Bhaarat\"</li></ul>",
        "spanish": "Elisión de la Schwa (Síncope): Eliminación automática de la vocal neutra implícita al final de palabra o en sílabas internas átonas. Ejemplo: \"Khabara\" &rarr; \"Khabr\".",
        "tags": ["languages_path", "hindi", "phonetics", "connected_speech", "schwa_deletion"]
    },
    {
        "deck": "03_Languages::Hindi::Phonetics::General",
        "scenario": "Hindi Phonetics 🗣️",
        "text": "In Hindi phonetics, the rule of {{c1::Aspirated 'H' Elision}} is defined as: The voiced glottal fricative /ɦ/ is weakened or omitted in fast speech, modifying surrounding vowels (e.g., *bahut* बहुत &rarr; \"baut\", *kahana* कहना &rarr; \"kana\").",
        "explanation": "Because aspiration requires high vocal energy, the /h/ sound is often elided in fast conversation, which can lead to vowel blending.",
        "usage": "Rule: <code>Aspirated 'H' Elision</code><br>Examples:<ul><li><code>bahut (very)</code> &rarr; \"baut\"</li><li><code>kahana (to say)</code> &rarr; \"kana\"</li><li><code>raha (stay)</code> &rarr; \"raa\"</li></ul>",
        "spanish": "Elisión de la 'H' aspirada: Omisión del fonema glotal /ɦ/ en el habla rápida, provocando la fusión de las vocales colindantes. Ejemplo: \"bahut\" &rarr; \"baut\".",
        "tags": ["languages_path", "hindi", "phonetics", "connected_speech", "h_elision"]
    },
    {
        "deck": "03_Languages::Hindi::Phonetics::General",
        "scenario": "Hindi Phonetics 🗣️",
        "text": "In Hindi phonetics, the rule of {{c1::Postposition Merger}} is defined as: Pronouns and their following postpositions fuse into a single word in writing and speech (e.g., *is me* इस में &rarr; \"isme\", *us ko* उस को &rarr; \"usko\").",
        "explanation": "Postpositions in Hindi behave similarly to prepositions in English. In speech, they form a single phonological word with the preceding pronoun, reducing transition time.",
        "usage": "Rule: <code>Postposition Merger</code><br>Examples:<ul><li><code>is me (in this)</code> &rarr; \"isme\"</li><li><code>us ko (to him/her)</code> &rarr; \"usko\"</li><li><code>kis liye (why)</code> &rarr; \"kisliye\"</li></ul>",
        "spanish": "Fusión de Posposiciones: Unión fonética de los pronombres con sus posposiciones para formar una sola unidad rítmica. Ejemplo: \"is me\" &rarr; \"isme\".",
        "tags": ["languages_path", "hindi", "phonetics", "connected_speech", "merger"]
    }
]

# 10. Cognitive Listening (New Deck under 03_Languages::General::Phonetics::Cognitive_Listening) - 8 Cards
cognitive_cards = [
    {
        "deck": "03_Languages::General::Phonetics::Cognitive_Listening",
        "scenario": "Cognitive Listening: The 3 Stages of Speech 🧠",
        "text": "In cognitive listening science, the model of {{c1::The 3 Stages of Speech}} (by Richard Cauldwell) describes three phases of language pronunciation: (1) **Garden Stage** (clear, dictionary pronunciation), (2) **Greenhouse Stage** (careful textbook speech), and (3) **Jungle Stage** (rapid, spontaneous native speech with deformations).",
        "explanation": "Language learners struggle in real life because they are trained in the structured rules of the Garden or Greenhouse stages, but native conversations occur in the Jungle, where sounds are compressed and blurred.",
        "usage": "The Three Stages:<ul><li><b>Garden</b>: Clear, isolated, dictionary citation form.</li><li><b>Greenhouse</b>: Textbook standard connected speech.</li><li><b>Jungle</b>: Physical sound deformation: Squish (compression), Stream (no pauses), and Blur (acoustic masking).</li></ul>",
        "spanish": "El Modelo de los 3 Estadios del Habla (Richard Cauldwell): Garden (Jardín - diccionario), Greenhouse (Invernadero - cuidado) y Jungle (Selva - espontáneo y deformado).",
        "tags": ["languages_path", "cognitive_listening", "cauldwell", "listening_theory"]
    },
    {
        "deck": "03_Languages::General::Phonetics::Cognitive_Listening",
        "scenario": "Cognitive Listening: Cauldwell's Jungle Rule 🧠",
        "text": "In cognitive listening science, Cauldwell's rule for decoding rapid speech is: Do not try to listen to every isolated word; instead, perform {{c1::Tonic Syllable Hunting}} (target the main stressed syllable of each rhythmic group) and let the context fill in the gaps.",
        "explanation": "Because fast speech compresses unstressed vowels and drops consonants, hunting for every single word is cognitively overwhelming. Locking onto the stressed syllables provides the anchor points for the brain to deduce meaning.",
        "usage": "Action: Practice 'Tonic Syllable Hunting' rather than word-for-word decoding. Identify the rhythmic beats of the sentence.",
        "spanish": "Regla de Cauldwell para la Selva: No busques descifrar cada vocablo; caza la Sílaba Tónica (Tonic Syllable Hunting) de cada compás y deduce el resto por el contexto.",
        "tags": ["languages_path", "cognitive_listening", "cauldwell", "listening_skills"]
    },
    {
        "deck": "03_Languages::General::Phonetics::Cognitive_Listening",
        "scenario": "Cognitive Listening: Perceptual Magnet Effect 🧠",
        "text": "In cognitive listening science, the {{c1::Perceptual Magnet Effect}} (Patricia Kuhl) explains that the adult brain creates magnets based on native phonemes, causing it to incorrectly map new foreign sounds to native categories (e.g. ship vs sheep).",
        "explanation": "Infants can distinguish all human speech sounds. By adulthood, the brain establishes strong neural 'magnets' for native language sounds. When exposed to foreign phonemes, the brain pulls them towards the closest native magnet, creating auditory confusion.",
        "usage": "Correction: Use Minimal Pair Ear Training to 'demagnetize' the native filter and build new distinct neural categories.",
        "spanish": "Imán Perceptual (Patricia Kuhl): Filtro neuronal del cerebro adulto que deforma los sonidos extranjeros, encajándolos a la fuerza en los fonemas de su lengua materna.",
        "tags": ["languages_path", "cognitive_listening", "kuhl", "perceptual_bias"]
    },
    {
        "deck": "03_Languages::General::Phonetics::Cognitive_Listening",
        "scenario": "Cognitive Listening: nPVI Metric (Rhythm) 📊",
        "text": "In acoustic linguistics, the rhythm of languages is measured using the {{c1::nPVI (Normalized Pairwise Variability Index)}}, where stress-timed languages (e.g. English, German) have a high index, while syllable-timed languages (e.g. Spanish, French) have a low index.",
        "explanation": "nPVI measures the variability in duration between adjacent vowels. Stress-timed languages compress unstressed vowels to schwas, leading to massive duration differences (high index). Syllable-timed languages give equal duration to syllables (low index, metronomic rhythm).",
        "usage": "Métricas:<ul><li>Stress-Timed (English, German): High nPVI (>65).</li><li>Syllable-Timed (Spanish, French, Italian): Low nPVI (<45).</li><li>Mora-Timed (Japanese): Ultra-low nPVI (<35).</li></ul>",
        "spanish": "Métrica nPVI: Clasificación acústica del ritmo lingüístico. Mide la variación de duración entre sílabas contiguas; alta en Stress-Timed (inglés) y baja en Syllable-Timed (español).",
        "tags": ["languages_path", "cognitive_listening", "rhythm", "npvi"]
    },
    {
        "deck": "03_Languages::General::Phonetics::Cognitive_Listening",
        "scenario": "Cognitive Listening: Speed-Ramping Method 🏃‍♂️",
        "text": "In language acquisition, the {{c1::Speed-Ramping Method}} conditions processing speed by listening to a short clip in a specific order: 0.8x (map junctions) &rarr; 1.0x &rarr; 1.25x (over-speed training) &rarr; 1.0x (now perceived as slow motion).",
        "explanation": "By forcing the brain to process speech at 1.25x speed, the subsequent return to 1.0x normal speed feels significantly slower, lowering the processing strain and enhancing comprehension.",
        "usage": "Routine: Take a 15-second audio clip. Listen: 0.8x &rarr; 1.0x &rarr; 1.25x (3 reps) &rarr; 1.0x (normal).",
        "spanish": "Método Speed-Ramping (Escalado de Velocidad): Entrenamiento del procesamiento neuro-auditivo acelerando y desacelerando el audio (0.8x &rarr; 1.0x &rarr; 1.25x &rarr; 1.0x).",
        "tags": ["languages_path", "cognitive_listening", "speed_ramping", "training_protocols"]
    },
    {
        "deck": "03_Languages::General::Phonetics::Cognitive_Listening",
        "scenario": "Cognitive Listening: Narrow Listening 🎧",
        "text": "In language acquisition, Stephen Krashen's {{c1::Narrow Listening}} technique involves consuming audio content from the **same speaker** on the **same topic** for 2-3 weeks to lower cognitive load by stabilizing the speaker's idiolect.",
        "explanation": "Each native speaker has a unique idiolect (speech patterns, pitch, preferred contractions). Keeping the speaker and topic stable allows the brain to map that individual's sounds easily, freeing up cognitive capacity to learn language structure.",
        "usage": "Action: Choose one podcaster/speaker on one specific topic, and consume their content exclusively for 2 weeks.",
        "spanish": "Narrow Listening (Escucha Estrecha): Consumo de contenido del mismo hablante y tema durante 2-3 semanas para familiarizarse con su idiolecto y reducir la fatiga mental.",
        "tags": ["languages_path", "cognitive_listening", "krashen", "narrow_listening"]
    },
    {
        "deck": "03_Languages::General::Phonetics::Cognitive_Listening",
        "scenario": "Cognitive Listening: Micro-Dictation ✍️",
        "text": "In language acquisition, the {{c1::Micro-Dictation}} protocol (Arguelles) consists of transcribing a 10-second fast native clip without subtitles, leaving gaps `[???]` for incomprehensible parts, and then checking which phonetic reduction rule caused the gap.",
        "explanation": "Transcribing short segments forces you to confront exactly what your brain missed. Comparing your draft with the transcript reveals your specific perceptual blind spots (e.g. not recognizing a dropped H or a glottal stop).",
        "usage": "Protocol: Transcribe 10s audio &rarr; mark gaps [???] &rarr; compare with text &rarr; log the elision/reduction rule.",
        "spanish": "Protocolo de Micro-Dictado (Arguelles): Transcripción de clips cortos marcando vacíos [???] para identificar qué regla de habla rápida causó la confusión auditiva.",
        "tags": ["languages_path", "cognitive_listening", "arguelles", "micro_dictation"]
    },
    {
        "deck": "03_Languages::General::Phonetics::Cognitive_Listening",
        "scenario": "Cognitive Listening: Pitch Contours 📉📈",
        "text": "In prosodic pragmatics, intonation contours carry structural meaning: a {{c1::Falling Pitch (📉)}} indicates certainty and WH-questions, a {{c2::Rising Pitch (📈)}} indicates Yes/No questions and lists, and a {{c3::Fall-Rise Pitch (📉📈)}} conveys politeness or reservations.",
        "explanation": "Pitch contours carry pragmatic context beyond words. High Rising Terminal (HRT) is a rising contour on statements used in Australian/American English to check for listener agreement.",
        "usage": "Contours:<ul><li>Falling (📉): 'Where is the station?' (Certainty/WH-question)</li><li>Rising (📈): 'Are you ready?' (Yes/No query)</li><li>Fall-Rise (📉📈): 'Well, I think so...' (Reservation/Politeness)</li></ul>",
        "spanish": "Contornos de Pitch (Entonación): Curvas tonales que aportan pragmática. Descendente (📉) para afirmaciones/WH-questions; Ascendente (📈) para Yes/No; Descendente-Ascendente (📉📈) para reservas.",
        "tags": ["languages_path", "cognitive_listening", "intonation", "pitch"]
    }
]

# ----------------- Main script execution -----------------

def run():
    print("=== REGISTERING PHONETICS MASTER GUIDE CARDS IN JSON DECKS ===")
    
    # 1. Update English Connected Speech JSON
    eng_path = DECKS_DIR / "03_Languages" / "English" / "Phonetics" / "Connected_Speech.json"
    eng_data = load_or_create_json(eng_path)
    # Check for duplicates based on 'text'
    existing_texts = {card["text"].strip() for card in eng_data}
    added_count = 0
    for card in english_cards:
        if card["text"].strip() not in existing_texts:
            eng_data.append(card)
            added_count += 1
    save_json(eng_path, eng_data)
    print(f"Added {added_count} new English connected speech cards.")

    # 2. Update Spanish General JSON
    es_path = DECKS_DIR / "03_Languages" / "Spanish" / "Phonetics" / "General.json"
    es_data = load_or_create_json(es_path)
    existing_texts = {card["text"].strip() for card in es_data}
    added_count = 0
    for card in spanish_cards:
        if card["text"].strip() not in existing_texts:
            es_data.append(card)
            added_count += 1
    save_json(es_path, es_data)
    print(f"Added {added_count} new Spanish phonetics cards.")

    # 3. Update Chinese General JSON
    zh_path = DECKS_DIR / "03_Languages" / "Chinese" / "Phonetics" / "General.json"
    zh_data = load_or_create_json(zh_path)
    existing_texts = {card["text"].strip() for card in zh_data}
    added_count = 0
    for card in chinese_cards:
        if card["text"].strip() not in existing_texts:
            zh_data.append(card)
            added_count += 1
    save_json(zh_path, zh_data)
    print(f"Added {added_count} new Chinese phonetics cards.")

    # 4. Update French General JSON
    fr_path = DECKS_DIR / "03_Languages" / "French" / "Phonetics" / "General.json"
    fr_data = load_or_create_json(fr_path)
    existing_texts = {card["text"].strip() for card in fr_data}
    added_count = 0
    for card in french_cards:
        if card["text"].strip() not in existing_texts:
            fr_data.append(card)
            added_count += 1
    save_json(fr_path, fr_data)
    print(f"Added {added_count} new French phonetics cards.")

    # 5. Update German General JSON
    de_path = DECKS_DIR / "03_Languages" / "German" / "Phonetics" / "General.json"
    de_data = load_or_create_json(de_path)
    existing_texts = {card["text"].strip() for card in de_data}
    added_count = 0
    for card in german_cards:
        if card["text"].strip() not in existing_texts:
            de_data.append(card)
            added_count += 1
    save_json(de_path, de_data)
    print(f"Added {added_count} new German phonetics cards.")

    # 6. Update Italian General JSON
    it_path = DECKS_DIR / "03_Languages" / "Italian" / "Phonetics" / "General.json"
    it_data = load_or_create_json(it_path)
    existing_texts = {card["text"].strip() for card in it_data}
    added_count = 0
    for card in italian_cards:
        if card["text"].strip() not in existing_texts:
            it_data.append(card)
            added_count += 1
    save_json(it_path, it_data)
    print(f"Added {added_count} new Italian phonetics cards.")

    # 7. Update Portuguese General JSON
    pt_path = DECKS_DIR / "03_Languages" / "Portuguese" / "Phonetics" / "General.json"
    pt_data = load_or_create_json(pt_path)
    existing_texts = {card["text"].strip() for card in pt_data}
    added_count = 0
    for card in portuguese_cards:
        if card["text"].strip() not in existing_texts:
            pt_data.append(card)
            added_count += 1
    save_json(pt_path, pt_data)
    print(f"Added {added_count} new Portuguese phonetics cards.")

    # 8. Update Japanese General JSON
    ja_path = DECKS_DIR / "03_Languages" / "Japanese" / "Phonetics" / "General.json"
    ja_data = load_or_create_json(ja_path)
    existing_texts = {card["text"].strip() for card in ja_data}
    added_count = 0
    for card in japanese_cards:
        if card["text"].strip() not in existing_texts:
            ja_data.append(card)
            added_count += 1
    save_json(ja_path, ja_data)
    print(f"Added {added_count} new Japanese phonetics cards.")

    # 9. Create Hindi General JSON
    hi_path = DECKS_DIR / "03_Languages" / "Hindi" / "Phonetics" / "General.json"
    hi_data = load_or_create_json(hi_path)
    existing_texts = {card["text"].strip() for card in hi_data}
    added_count = 0
    for card in hindi_cards:
        if card["text"].strip() not in existing_texts:
            hi_data.append(card)
            added_count += 1
    save_json(hi_path, hi_data)
    print(f"Added {added_count} new Hindi phonetics cards.")

    # 10. Create Cognitive Listening JSON
    cog_path = DECKS_DIR / "03_Languages" / "General" / "Phonetics" / "Cognitive_Listening.json"
    cog_data = load_or_create_json(cog_path)
    existing_texts = {card["text"].strip() for card in cog_data}
    added_count = 0
    for card in cognitive_cards:
        if card["text"].strip() not in existing_texts:
            cog_data.append(card)
            added_count += 1
    save_json(cog_path, cog_data)
    print(f"Added {added_count} new Cognitive Listening cards.")

    # 11. Rebuild index.json
    rebuild_index()

if __name__ == "__main__":
    run()
