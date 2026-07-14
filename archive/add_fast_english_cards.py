import json
import os

database_file = "anki_cards_database.json"

if not os.path.exists(database_file):
    print(f"Error: {database_file} not found.")
    exit(1)

with open(database_file, "r", encoding="utf-8") as f:
    cards = json.load(f)

new_cards = [
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Flap T ⚡",
        "text": "In American English, a /t/ between two vowels (when the second is unstressed) turns into a {{c1::Flap T [ɾ]}}, making \"put it on\" sound like \"pur-id-on\".",
        "explanation": "The Flap T (or tap) is a sound made by briefly tapping the tongue tip against the alveolar ridge. It is acoustically identical to the Spanish single 'r' or a light 'd'. It allows speakers to bridge vowels without stopping the voice.",
        "usage": "Practice Drills:<ul><li><code>Get it out</code> &rarr; \"ged-id-out\"</li><li><code>What a day</code> &rarr; \"whad-a-day\"</li><li><code>Write a book</code> &rarr; \"wry-duh-book\"</li></ul><br>Reference: Learn more on <a href=\"https://www.youtube.com/@RachelsEnglish\">Rachel's English</a> (search: 'Rachel's English Flap T').",
        "spanish": "En inglés americano, la /t/ entre dos vocales se convierte en una 'Flap T' [ɾ] (como la 'r' suave en español). Por eso, \"put it on\" suena como \"pur-id-on\".",
        "tags": ["english", "phonetics", "connected_speech", "flap_t", "pronunciation"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: T + Y Coalescence 🤝",
        "text": "When a word ending in /t/ meets a word beginning with /y/, they merge into a {{c1::/tʃ/ (\"ch\" as in chair)}} sound. E.g., \"meet you\" is pronounced \"meetchu\".",
        "explanation": "This is a type of assimilation called coalescence (or palatalization). The mouth prepares for the palatal /y/ while pronouncing the alveolar /t/, resulting in the postalveolar affricate /tʃ/.",
        "usage": "Practice Drills:<ul><li><code>don't you</code> &rarr; \"donchoo\"</li><li><code>what you need</code> &rarr; \"whachoo need\"</li><li><code>can't you</code> &rarr; \"canchoo\"</li></ul><br>Reference: Look up \"Assimilation in English\" on <a href=\"https://www.youtube.com/@EnglishwithGreg\">English with Greg</a>.",
        "spanish": "Cuando una palabra que termina en /t/ se une con una que empieza con /y/, se fusionan en el sonido /tʃ/ ('ch'). Ejemplo: \"meet you\" &rarr; \"meetchu\".",
        "tags": ["english", "phonetics", "connected_speech", "coalescence", "pronunciation"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: D + Y Coalescence 🤝",
        "text": "When a word ending in /d/ meets a word beginning with /y/, they merge into a {{c1::/dʒ/ (\"j\" as in judge)}} sound. E.g., \"would you\" is pronounced \"woodja\".",
        "explanation": "Similar to T+Y coalescence, the voiced alveolar stop /d/ and palatal glide /y/ combine to form the voiced postalveolar affricate /dʒ/.",
        "usage": "Practice Drills:<ul><li><code>could you</code> &rarr; \"couldja\"</li><li><code>did you</code> &rarr; \"didja\"</li><li><code>find you</code> &rarr; \"findja\"</li></ul><br>Reference: Practice shadowing with \"Hadar Shemesh connected speech\" on YouTube.",
        "spanish": "Cuando una palabra que termina en /d/ se une con una que empieza con /y/, se fusionan en el sonido /dʒ/ ('y' o 'j' fuerte). Ejemplo: \"would you\" &rarr; \"woodja\".",
        "tags": ["english", "phonetics", "connected_speech", "coalescence", "pronunciation"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Glottal Stop 🤐",
        "text": "Before a consonant sound, a final /t/ is often not released, but stopped in the throat as a {{c1::Glottal Stop [ʔ]}}. E.g., \"not yet\" becomes \"no' yet\".",
        "explanation": "A glottal stop is produced by blocking the airflow in the vocal tract (specifically the glottis) rather than using the tongue to release air. This is a hallmark of native speakers trying to conserve energy.",
        "usage": "Practice Drills:<ul><li><code>flat tire</code> &rarr; \"fla' tire\"</li><li><code>button</code> &rarr; \"bu'n\"</li><li><code>football</code> &rarr; \"foo'ball\"</li></ul><br>Watch: \"Glottal Stop vs. Stop T\" on <a href=\"https://www.youtube.com/@RachelsEnglish\">Rachel's English</a>.",
        "spanish": "Antes de una consonante, la /t/ final a menudo se detiene en la garganta (parada glotal [ʔ]) en lugar de liberarse. Ejemplo: \"not yet\" &rarr; \"no' yet\".",
        "tags": ["english", "phonetics", "connected_speech", "glottal_stop", "pronunciation"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Liaison 🔗",
        "text": "To maintain a steady rhythm, native speakers link a final consonant to a following initial vowel, so that \"{{c1::turn on}}\" sounds like \"tur-non\".",
        "explanation": "This is known as liaison. In English, a word-final consonant behaves as if it belongs to the onset of the next syllable if that syllable starts with a vowel, avoiding breaks in airflow.",
        "usage": "Practice Drills:<ul><li><code>an apple</code> &rarr; \"a-napple\"</li><li><code>hold on</code> &rarr; \"hol-don\"</li><li><code>read it</code> &rarr; \"rea-dit\"</li></ul>",
        "spanish": "Para mantener un ritmo constante, los nativos enlazan la consonante final con la vocal inicial siguiente. Ejemplo: \"turn on\" suena como \"tur-non\".",
        "tags": ["english", "phonetics", "connected_speech", "liaison", "pronunciation"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: /w/ Intrusion 🔗",
        "text": "When linking a rounded vowel (e.g. oo, oh, ow) to another vowel, native speakers insert an intrusive {{c1::/w/ sound}}. E.g., \"go out\" is pronounced \"go-w-out\".",
        "explanation": "When the lips are rounded for the first vowel, the mouth naturally glides through a /w/ shape to transition to the next vowel, preventing an unnatural glottal break.",
        "usage": "Practice Drills:<ul><li><code>do it</code> &rarr; \"do-w-it\"</li><li><code>you are</code> &rarr; \"you-w-are\"</li><li><code>how about</code> &rarr; \"how-w-about\"</li></ul>",
        "spanish": "Al conectar una vocal redondeada (como /u/ o /o/) con otra vocal, se inserta naturalmente un sonido /w/ de transición. Ejemplo: \"go out\" &rarr; \"go-w-out\".",
        "tags": ["english", "phonetics", "connected_speech", "intrusion", "pronunciation"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: /j/ Intrusion 🔗",
        "text": "When linking a front vowel (e.g. ee, ay, ie) to another vowel, native speakers insert an intrusive {{c1::/j/ (or 'y') sound}}. E.g., \"he is\" is pronounced \"he-y-is\".",
        "explanation": "Because the tongue is high and forward for the first vowel, the transition to the next vowel naturally produces a palatal glide /j/ (\"y\" sound).",
        "usage": "Practice Drills:<ul><li><code>she agrees</code> &rarr; \"she-y-agrees\"</li><li><code>I am</code> &rarr; \"I-y-am\"</li><li><code>the end</code> &rarr; \"the-y-end\"</li></ul>",
        "spanish": "Al conectar una vocal anterior/alta (como /i/ o /ai/) con otra vocal, se introduce un sonido de transición /j/ (\"y\"). Ejemplo: \"he is\" &rarr; \"he-y-is\".",
        "tags": ["english", "phonetics", "connected_speech", "intrusion", "pronunciation"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Twin Consonants 👯",
        "text": "When a word ends with the same consonant sound that the next word begins with, native speakers {{c1::elongate or hold the sound}} instead of pronouncing it twice.",
        "explanation": "This is called gemination. Pronouncing both consonants individually requires stopping and restarting airflow, which hinders speech flow. Instead, a single, elongated consonant is produced.",
        "usage": "Practice Drills:<ul><li><code>black cat</code> &rarr; \"bla-cat\" (held /k/)</li><li><code>bad dog</code> &rarr; \"ba-dog\" (held /d/)</li><li><code>social life</code> &rarr; \"socia-life\" (held /l/)</li><li><code>gas station</code> &rarr; \"ga-station\" (held /s/)</li></ul>",
        "spanish": "Cuando una palabra termina con la misma consonante con la que empieza la siguiente, se alarga el sonido de la consonante en lugar de pronunciarla dos veces. Ejemplo: \"black cat\" &rarr; \"bla-cat\".",
        "tags": ["english", "phonetics", "connected_speech", "gemination", "pronunciation"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: H-Dropping 💨",
        "text": "In fast speech, the /h/ sound in unstressed pronouns (he, him, his, her) is often {{c1::elided (dropped)}}, causing \"tell him\" to sound like \"tell-im\".",
        "explanation": "Because grammatical pronouns are unstressed, speakers drop the /h/ to save vocal effort. The final consonant of the preceding word then links directly to the pronoun's remaining vowel.",
        "usage": "Practice Drills:<ul><li><code>ask her</code> &rarr; \"ask-er\"</li><li><code>what did he say</code> &rarr; \"what-dide-say\"</li><li><code>is he here</code> &rarr; \"is-e-here\"</li></ul><br>Warning: Do not drop the /h/ if the pronoun is stressed or at the beginning of a sentence.",
        "spanish": "En el habla rápida, la /h/ en pronombres átonos (him, her, etc.) suele omitirse, haciendo que \"tell him\" suene como \"tell-im\".",
        "tags": ["english", "phonetics", "connected_speech", "elision", "h_drop"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Consonant Elision 💨",
        "text": "When /t/ or /d/ is sandwiched between two other consonants, it is often {{c1::dropped entirely}} to ease pronunciation. E.g., \"last night\" becomes \"las-night\".",
        "explanation": "Three consonants in a row (like /st/ and /n/ in \"last night\") require complex tongue movement. Dropping the middle alveolar stop (/t/ or /d/) allows a smoother transition.",
        "usage": "Practice Drills:<ul><li><code>next door</code> &rarr; \"nex-door\"</li><li><code>hold tight</code> &rarr; \"hole-tight\"</li><li><code>you and me</code> &rarr; \"you n me\"</li><li><code>we went to</code> &rarr; \"we wen-to\"</li></ul>",
        "spanish": "Cuando /t/ o /d/ están entre otras dos consonantes, a menudo se omiten por completo. Ejemplo: \"last night\" &rarr; \"las-night\".",
        "tags": ["english", "phonetics", "connected_speech", "elision", "consonants"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Weak \"To\" 📉",
        "text": "In unstressed positions, the preposition \"to\" is reduced from /tuː/ to {{c1::/tə/ (sounding like \"tuh\")}} before consonants. E.g., \"try to run\" &rarr; \"try-tuh run\".",
        "explanation": "English is stress-timed. Functional words like \"to\" reduce their vowels to the neutral schwa /ə/ when they do not carry main sentence stress, helping emphasize content words.",
        "usage": "Practice Drills:<ul><li><code>nice to meet you</code> &rarr; \"nice-tuh meet you\"</li><li><code>I need to go</code> &rarr; \"I need-tuh go\"</li><li><code>have to do</code> &rarr; \"have-tuh do\" (becomes \"hafta\")</li></ul>",
        "spanish": "La preposición \"to\" en posiciones átonas se reduce a \"tuh\" /tə/ (schwa). Ejemplo: \"try to run\" &rarr; \"try-tuh run\".",
        "tags": ["english", "phonetics", "connected_speech", "reductions", "weak_forms"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Weak \"For\" 📉",
        "text": "The preposition \"for\" is unstressed in sentences and reduces from /fɔːr/ to {{c1::/fər/ (sounding like \"fer\")}}, as in \"this is for you\" &rarr; \"this is fer-you\".",
        "explanation": "Vowel reduction turns the full vowel /ɔː/ into an r-colored schwa /ɚ/ or /ər/. The full pronunciation /fɔː/ is reserved for when the word is stressed or at the end of a clause.",
        "usage": "Practice Drills:<ul><li><code>for free</code> &rarr; \"fer-free\"</li><li><code>for example</code> &rarr; \"fer-example\"</li><li><code>waiting for a cab</code> &rarr; \"waiting fer-a cab\"</li></ul>",
        "spanish": "La palabra \"for\" se reduce a \"fer\" /fər/ cuando no está acentuada en una frase. Ejemplo: \"this is for you\" suena como \"this is fer-you\".",
        "tags": ["english", "phonetics", "connected_speech", "reductions", "weak_forms"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Weak \"And\" 📉",
        "text": "The conjunction \"and\" is unstressed and heavily reduced, dropping both its vowel and its final /d/, leaving only {{c1::/n/ or /ən/}}. E.g., \"black and white\" becomes \"black n white\".",
        "explanation": "In rapid speech, \"and\" is shortened to a syllabic /n/ sound. The /d/ is only pronounced if followed by a vowel and spoken slowly, or when emphasizing addition.",
        "usage": "Practice Drills:<ul><li><code>rock and roll</code> &rarr; \"rock n roll\"</li><li><code>you and me</code> &rarr; \"you n me\"</li><li><code>chips and dip</code> &rarr; \"chips n dip\"</li></ul>",
        "spanish": "La conjunción \"and\" pierde su vocal y su /d/, reduciéndose al simple sonido nasal \"n\" /n/ o /ən/. Ejemplo: \"black and white\" suena como \"black n white\".",
        "tags": ["english", "phonetics", "connected_speech", "reductions", "weak_forms"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Weak \"Of\" 📉",
        "text": "The preposition \"of\" reduces its vowel and drops the /v/ before consonants, sounding like {{c1::/ə/ (\"uh\" or \"a\")}}. E.g., \"cup of tea\" becomes \"cup-a tea\".",
        "explanation": "The /v/ is elided when followed by a consonant to avoid awkward transitions. When followed by a vowel, the /v/ is usually kept and linked (e.g., \"out of office\" &rarr; \"out-uh-voffice\").",
        "usage": "Practice Drills:<ul><li><code>lots of time</code> &rarr; \"lots-a time\"</li><li><code>piece of cake</code> &rarr; \"piece-a cake\"</li><li><code>out of here</code> &rarr; \"outta here\"</li></ul>",
        "spanish": "La preposición \"of\" se acorta a un simple sonido \"a\" /ə/ (schwa) antes de una consonante. Ejemplo: \"cup of tea\" &rarr; \"cup-a tea\".",
        "tags": ["english", "phonetics", "connected_speech", "reductions", "weak_forms"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: S + Y Assimilation 🤝",
        "text": "When a word ending in /s/ meets a word starting with /y/, they assimilate into a {{c1::/ʃ/ (\"sh\" as in shoe)}} sound. E.g., \"bless you\" becomes \"blesh-you\".",
        "explanation": "The alveolar fricative /s/ and the palatal approximant /y/ coalesce into the postalveolar fricative /ʃ/. The tongue shifts back slightly, combining the two articulations into one.",
        "usage": "Practice Drills:<ul><li><code>this year</code> &rarr; \"thisheer\"</li><li><code>dress you</code> &rarr; \"dresh-you\"</li><li><code>press your luck</code> &rarr; \"presh-your luck\"</li></ul>",
        "spanish": "El encuentro de /s/ y /y/ produce el sonido de la \"sh\" inglesa /ʃ/. Ejemplo: \"bless you\" suena como \"blesh-you\".",
        "tags": ["english", "phonetics", "connected_speech", "assimilation"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Z + Y Assimilation 🤝",
        "text": "When a word ending in /z/ meets a word starting with /y/, they assimilate into a {{c1::/ʒ/ (\"zh\" as in measure)}} sound. E.g., \"how's your day\" becomes \"how-zher day\".",
        "explanation": "The voiced alveolar fricative /z/ and the palatal approximant /y/ coalesce into the voiced postalveolar fricative /ʒ/. This is the voiced equivalent of the S+Y assimilation.",
        "usage": "Practice Drills:<ul><li><code>where's your car</code> &rarr; \"where-zher car\"</li><li><code>as you know</code> &rarr; \"azh-you know\"</li><li><code>close your eyes</code> &rarr; \"clozh-your eyes\"</li></ul>",
        "spanish": "La combinación de /z/ y /y/ genera el sonido /ʒ/ (la 'y' argentina o la 's' en 'measure'). Ejemplo: \"how's your\" suena como \"how-zher\".",
        "tags": ["english", "phonetics", "connected_speech", "assimilation"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Dark L Vocalization 🌑",
        "text": "At the end of words or before consonants, the \"Dark L\" [ɫ] is often vocalized, sounding like a {{c1::vowel-like /oʊ/ or /ʊ/ (\"uh\")}} rather than a consonant. E.g., \"feel\" &rarr; \"fee-uh\".",
        "explanation": "In many dialects of English, the tongue tip does not touch the roof of the mouth for a word-final L. Instead, only the back of the tongue is raised, turning the L into a back vowel sound.",
        "usage": "Practice Drills:<ul><li><code>milk</code> &rarr; \"mi-uk\"</li><li><code>tall</code> &rarr; \"taw-uh\"</li><li><code>real</code> &rarr; \"ree-uh\"</li></ul>",
        "spanish": "La 'L' al final de las palabras (Dark L) a menudo se vocaliza en la parte trasera de la boca, sonando similar a una 'u' o 'o'. Ejemplo: \"feel\" suena como \"fee-uh\".",
        "tags": ["english", "phonetics", "connected_speech", "dark_l"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: G-Dropping 🏃‍♂️",
        "text": "In casual speech, the velar nasal sound /ŋ/ at the end of \"-ing\" verbs is reduced to the alveolar nasal {{c1::/n/}}, so that \"working\" is spoken as \"workin'\".",
        "explanation": "This is a highly common reduction where the point of articulation shifts from the back of the mouth (velar /ŋ/) to the front (alveolar /n/). This is often represented spelling-wise with an apostrophe.",
        "usage": "Practice Drills:<ul><li><code>What are you doing?</code> &rarr; \"What-ya doin'?\"</li><li><code>nothing</code> &rarr; \"nothin'\"</li><li><code>running late</code> &rarr; \"runnin' late\"</li></ul>",
        "spanish": "En contextos informales, el sonido \"-ing\" nasal se acorta al sonido simple de la \"n\". Ejemplo: \"working\" suena como \"workin'\".",
        "tags": ["english", "phonetics", "connected_speech", "g_drop", "informal"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: Positive \"Can\" vs. \"Can't\" 👂",
        "text": "In native speech, the positive auxiliary \"can\" is reduced to {{c1::/kən/ (\"kun\")}}, while the negative \"can't\" retains a clear stressed vowel /kænt/ or uses a glottal stop /kæn'/.",
        "explanation": "Because positive \"can\" is a grammatical helper, it is unstressed and reduces to schwa. The negative \"can't\" contains the core negative meaning, so it remains stressed and retains its full vowel, making stress the primary cue to tell them apart.",
        "usage": "Contrastive Drills:<ul><li><code>I can do it</code> &rarr; \"I kun do it\"</li><li><code>I can't do it</code> &rarr; \"I caan' do it\" (longer vowel, stop T)</li></ul>",
        "spanish": "El afirmativo \"can\" se reduce a un rápido \"kun\" /kən/, mientras que el negativo \"can't\" se acentúa con una vocal larga y clara o parada glotal. La clave está en el ritmo y el acento.",
        "tags": ["english", "phonetics", "connected_speech", "can_cant", "listening"]
    },
    {
        "deck": "English::Phonetics::Connected_Speech",
        "scenario": "Fast English: \"What are you\" &rarr; Whatcha 🗣",
        "text": "In highly casual speech, the entire phrase \"What are you...\" is reduced and merged into the single word {{c1::\"whatcha\" /wɒtʃə/}}. E.g., \"What are you doing?\" becomes \"Whatcha doin'?\".",
        "explanation": "This involves multiple reductions: \"are\" is reduced to a schwa or omitted, and \"what\" links to \"you\" via T+Y coalescence, forming \"whatcha\".",
        "usage": "Practice Drills:<ul><li><code>What are you talking about?</code> &rarr; \"Whatcha talkin' 'bout?\"</li><li><code>What are you thinking?</code> &rarr; \"Whatcha thinkin'?\"</li></ul><br>Reference: Learn about spoken reductions in Rachel's English videos.",
        "spanish": "En el habla informal, toda la frase \"What are you...\" se comprime y pronuncia como \"whatcha\" (/wɒtʃə/). Ejemplo: \"What are you doing?\" &rarr; \"Whatcha doin'?\".",
        "tags": ["english", "phonetics", "connected_speech", "reductions", "informal"]
    }
]

existing_scenarios = {c["scenario"] for c in cards}
added_count = 0

for card in new_cards:
    if card["scenario"] not in existing_scenarios:
        cards.append(card)
        added_count += 1

with open(database_file, "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print(f"Successfully added {added_count} new cards. Total cards in database: {len(cards)}.")
