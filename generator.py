#!/usr/bin/env python3
"""Phonetics Corpus Generator — LLM-Orchestrated Anki Card Factory.

System prompt architecture based on the "Computational Phonetics Linguist" role
designed for precision acoustic data generation with Gemini API.

Usage:
    python generator.py --rule 2                     # Flap T, 15 cards (default)
    python generator.py --rule 2 --count 25          # Flap T, 25 cards
    python generator.py --rule 0 --template T8       # Minimal Pairs
    python generator.py --all --count 15             # All 18 rules
    python generator.py --list                       # Show rule catalog
    python generator.py --dry-run --rule 2           # Show prompt without calling API

Available rules (--rule N):
    0  = Minimal Pairs (T8_MinimalPair template)
    1  = 3-Consonant Cluster Elision
    2  = Flap T / Intervocalic Flapping
    3  = Glottal Stop [ʔ]
    4  = Nasal T-Deletion (after /n/)
    5  = Yod Coalescence (don't you / would you)
    6  = C+V Linking / Resyllabification
    7  = Weak H-Dropping (him, her, his)
    8  = Schwa /ə/ Reduction (Vowel Reduction)
    9  = Linking R & Intrusive R (UK/AU)
    10 = Lexical Chunks (gonna, wanna, gotta)
    11 = Dark L & L-Vocalization
    12 = Intrusive Glides /w/ and /j/
    13 = Unreleased Stops (held plosives)
    14 = Stress-Timed Rhythm & Isochrony
    15 = Flap D (Intervocalic D Flapping)
    16 = Pre-Glottalization (Glottal Reinforcement)
    17 = Advanced Auxiliary Chunks
    18 = Syllabic Consonants
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).parent.resolve()
DECKS_PHONETICS = (
    BASE_DIR / "decks" / "03_Languages" / "English"
    / "Phonetics" / "Connected_Speech_Patterns"
)
sys.path.insert(0, str(BASE_DIR))

from audio_links_registry import (
    build_chunk_audio, build_minimal_pair_audio,
    youglish_url, forvo_url, ipa_chart_url,
)
from card_validator import sanitize_and_validate_card
from gemini_provider import get_api_key

import requests

# ---------------------------------------------------------------------------
# GEMINI CONFIG
# ---------------------------------------------------------------------------
GEMINI_API_KEY = get_api_key()
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"
)
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0  # seconds


# ============================================================
# BASE SYSTEM PROMPT — Computational Phonetics Linguist role
# (Based on user-validated prompt architecture)
# ============================================================
BASE_SYSTEM_PROMPT = """\
You are a computational linguist specializing in acoustic phonetics, connected speech
(fast native speech), and structured data engineering for spaced-repetition systems.

Your task is to generate a corpus of Anki flashcard examples for specific phonetic rules.

OUTPUT FORMAT — Respond EXCLUSIVELY with a valid JSON object. No Markdown, no explanatory text.

GENERATION RULES:
1. Examples must reflect natural, colloquial, modern language (Cauldwell's "Jungle Stage").
   Avoid overly formal or academic speech patterns.
2. IPA transcriptions must reflect REAL pronunciation (with elisions, assimilations,
   and reductions) — NOT strict dictionary pronunciation.
3. Each example must clearly isolate the requested phonetic phenomenon.
4. 'connected_form' must accurately represent the native phonetic compression.
5. 'rules_applied' must list ALL phonetic rules triggered (not just the target rule).
6. 'spanish' must be a natural, accurate translation of the context.
7. Generate cards across 3 tiers: Tier 1 (isolated), Tier 2 (combined), Tier 3 (native chunk).

JSON SCHEMA (T9_ListeningChunk — use this unless instructed otherwise):
{
  "rule_applied": "<rule name>",
  "cards": [
    {
      "scenario": "<Category prefix + emoji> (e.g. 'Fast English: Flap T ⚡ — Tier 1')",
      "full_transcript": "<exact written English phrase>",
      "connected_form": "<how a native speaker actually says it>",
      "ipa_transcription": "<IPA for the connected form>",
      "gap_text": "<written phrase with {{c1::connected_form}} cloze substitution>",
      "rules_applied": ["<rule1>", "<rule2>"],
      "audio_search_forvo": "<exact word or phrase for Forvo>",
      "audio_search_youglish": "<exact phrase for YouGlish search>",
      "phonetic_breakdown": "<1-2 sentence explanation of the phonetic change and muscular movement>",
      "spanish": "<natural Spanish translation of the phrase and context>",
      "tier": 1
    }
  ]
}

Tier guide:
  1 = Isolated single pattern (single word or 2-word phrase, 1 rule only)
  2 = Combined (multi-word phrase, 2-3 rules simultaneously)
  3 = Native chunk (full conversational sentence, 3-5 rules, shadowing-ready)
"""

# ============================================================
# T8 SYSTEM PROMPT — Minimal Pairs
# ============================================================
T8_SYSTEM_PROMPT = """\
You are a computational linguist specializing in acoustic phonetics and phoneme
discrimination training (Patricia Kuhl Perceptual Magnet demagnetization method).

Generate minimal pair cards for Anki in STRICT JSON format only.

JSON SCHEMA (T8_MinimalPair):
{
  "rule_applied": "Minimal Pairs — Phoneme Discrimination",
  "cards": [
    {
      "phoneme_a": "/ɪ/",
      "phoneme_b": "/iː/",
      "ipa_a": "short, relaxed, mid-high front vowel",
      "ipa_b": "long, tense, high front vowel",
      "word_pairs": [
        ["ship", "sheep", "/ʃɪp/", "/ʃiːp/"],
        ["bit", "beat", "/bɪt/", "/biːt/"],
        ["sit", "seat", "/sɪt/", "/siːt/"]
      ],
      "muscle_tip": "<Spanish: articulatory instruction for producing both phonemes correctly>",
      "audio_search_phoneme_a": "<word for Forvo — the more difficult phoneme for Spanish speakers>",
      "audio_search_phoneme_b": "<word for Forvo>",
      "language": "en",
      "spanish": "<Spanish explanation of the perceptual challenge>"
    }
  ]
}

Generate each card as ONE phoneme pair with 8-12 word_pairs examples.
Focus on pairs confusing for Spanish L1 speakers.
"""


# ============================================================
# RULE CATALOG — 18 English Connected Speech Patterns + Minimal Pairs
# ============================================================
RULE_CATALOG: Dict[int, Dict[str, Any]] = {
    0: {
        "name": "Minimal_Pairs",
        "deck": "03_Languages::English::Phonetics::CS_00_Minimal_Pairs",
        "file": "00_Minimal_Pairs.json",
        "template": "T8_MinimalPair",
        "system_prompt": T8_SYSTEM_PROMPT,
        "user_prompt": """\
Generate 12 phoneme discrimination cards (T8_MinimalPair) targeting the most confusing
English phoneme pairs for Spanish native speakers.

PAIRS TO COVER (one card per pair):
1.  /ɪ/ vs /iː/ — ship vs sheep, bit vs beat
2.  /ʌ/ vs /ɑː/ — cup vs car, cut vs cart
3.  /v/ vs /b/ — very vs berry, vat vs bat
4.  /θ/ vs /s/ — think vs sink, three vs see
5.  /ð/ vs /d/ — this vs dis, they vs day
6.  /æ/ vs /ɛ/ — bad vs bed, man vs men
7.  /æ/ vs /ɑː/ — cat vs cart, bat vs bar
8.  /ʊ/ vs /uː/ — foot vs food, could vs cooed
9.  /ɒ/ vs /oʊ/ (UK vs US) — lot vs note
10. /p/ vs /b/ word-final — cap vs cab, cup vs cub
11. /tʃ/ vs /ʃ/ — cheap vs sheep, chain vs Shane
12. /dʒ/ vs /j/ — jell vs yell, jaw vs yaw

Include 8-10 word_pairs per card. Make muscle_tip practical and specific.
""",
    },
    1: {
        "name": "Cluster_Elision",
        "deck": "03_Languages::English::Phonetics::CS_01_Cluster_Elision",
        "file": "01_Cluster_Elision.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for the 3-Consonant Cluster Elision rule.

RULE: When 3+ consonants cluster together, the MIDDLE consonant (/t/ or /d/) disappears.
This happens within words AND across word boundaries.

REFERENCE EXAMPLES (from master phonetics table):
- "last night" → /læs naɪt/ → "Las-night"
- "next door" → /neks dɔːr/ → "Nex-door"
- "must be" → /məs bi/ → "Mus-be"
- "just one" → /dʒʌs wʌn/ → "Jus-one"

MORE EXAMPLES TO DRAW FROM:
  Within-word: facts, acts, texts, lists, guests, tests, costs, rests, mists
  Cross-boundary: best friend, cold drink, old tricks, soft drink, hand shake,
                  wind storm, kind thought, round trip, past tense, left side

TIER BREAKDOWN:
  Tier 1 (5 cards): Single word or 2-word phrase, one cluster, slow enough to catch
  Tier 2 (5 cards): 4-6 word phrase, cluster elision + Schwa reduction
  Tier 3 (5 cards): Full colloquial sentence, 2+ elisions + other rules

CRITICAL: Only elisions that native Americans ACTUALLY make. No hypercorrections.
""",
    },
    2: {
        "name": "Flap_T",
        "deck": "03_Languages::English::Phonetics::CS_02_Flap_T",
        "file": "02_Flap_T.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for the Flap T / Intervocalic Flapping rule.

RULE: The /t/ (or /tt/) between two vowels becomes a voiced alveolar tap [ɾ] when
the FOLLOWING vowel is unstressed. The [ɾ] is acoustically identical to Spanish 'r' in "pero".
Crucially, this also occurs ACROSS WORD BOUNDARIES when the last consonant of word 1
is /t/ and word 2 starts with an unstressed vowel.

REFERENCE EXAMPLES:
- "water" → /ˈwɑː.ɾər/ → "Wa-der" (within word)
- "put it on" → /pʊ.ɾɪ.ɾɑːn/ → "Pu-di-ron" (DOUBLE flap crossing 3 words)
- "better" → /ˈbɛ.ɾər/ → "Be-rer"
- "What a cool day" → /wʌ.ɾə kuːl deɪ/ → "Wa-ra cool day"

MORE VOCABULARY: city/ci-dy, butter/bu-der, writing/wri-ding, pretty/pri-dy,
bitter/bi-der, later/lay-der, data/day-da, pity/pi-dy, atom/a-dom,
getting/ge-ding, putting/pu-ding, hitting/hi-ding, sitting/si-ding,
get it/ge-did, let it/le-did, set it/se-did, take it/tay-kid, make it/may-kid

TIER BREAKDOWN:
  Tier 1 (5 cards): Single word with internal flap (water, butter, city)
  Tier 2 (5 cards): 2-3 word phrase with cross-boundary flap (put it on, get a job)
  Tier 3 (5 cards): Full sentence with 3+ flaps (colloq. native speed)

Explicitly note in phonetic_breakdown: "The [ɾ] is NOT a D or a T. It's a single rapid tap."
""",
    },
    3: {
        "name": "Glottal_Stop",
        "deck": "03_Languages::English::Phonetics::CS_03_Glottal_Stop",
        "file": "03_Glottal_Stop.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for the Glottal Stop [ʔ] rule.

RULE: The /t/ is replaced by a glottal stop [ʔ]:
  - American English: before syllabic /n/ (button, mountain, written)
  - British RP/Cockney: before any consonant OR at syllable boundaries (bottle, important)
  - Both: at the end of utterances for emphasis

REFERENCE EXAMPLES:
- "button" → /ˈbʌ.ʔn̩/ → "Bu'n" (micro-pause, no tongue tip)
- "important" → /ɪmˈpɔː.ʔn̩t/ → "Impor'n't"
- "bottle" → /ˈbɒ.ʔl̩/ → "Bo'l" (British)
- "I can't go" → /aɪ kænʔ ɡoʊ/ → "I can' go"
- "Manhattan" → /mæˈhæ.ʔn̩/ → "Manh-a'n"

MORE: curtain, certain, Britain, cotton, kitten, mitten, bitten, beaten, eaten,
      captain, Latin, satin, beaten, flatten, rotten, fatten, gotten, lighten

MARK CLEARLY: Is this American (before /n/ only) or British (broader)?
""",
    },
    4: {
        "name": "Nasal_T_Deletion",
        "deck": "03_Languages::English::Phonetics::CS_04_Nasal_T_Deletion",
        "file": "04_Nasal_T_Deletion.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Nasal T-Deletion (after /n/).

RULE: After /n/ in an UNSTRESSED syllable, the /t/ completely vanishes.
This is extremely common in natural conversational American English.

REFERENCE EXAMPLES:
- "internet" → /ˈɪn.nər.nɛt/ → "Inn-er-net"
- "twenty" → /ˈtwɛn.i/ → "Twen-y"
- "center" → /ˈsɛn.ər/ → "Sen-er"
- "international" → /ˌɪn.nərˈnæʃ.nəl/ → "Inner-national"

MORE WORDS: winter/winner, enter/inner, painter/pain-er, printed/prinn-ed,
winter/winn-er, rented/renn-ed, wanted/wann-ed, planted/plann-ed,
counted/counn-ed, pointed/poinn-ed, fountain/foun-in, mountain/moun-in,
interview/inn-erview, interesting/inn-eresting, continental/conn-inental

INCLUDE also cross-boundary: "don't tell" → "don-tell", "can't do it" → "can-do-it"
""",
    },
    5: {
        "name": "Yod_Coalescence",
        "deck": "03_Languages::English::Phonetics::CS_05_Yod_Coalescence",
        "file": "05_Yod_Coalescence.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Yod Coalescence / Palatal Assimilation.

RULE: When these consonants meet the /j/ "y-sound" of YOU/YOUR/YEAR, they fuse:
  /t/ + /j/ → /tʃ/ (CH): "don't you" = "DON-CHOO"
  /d/ + /j/ → /dʒ/ (J):  "would you" = "WOOD-JOO"
  /s/ + /j/ → /ʃ/ (SH):  "miss you"  = "MI-SHOO"
  /z/ + /j/ → /ʒ/ (ZH):  "as you know" = "A-ZHOO know"

REFERENCE EXAMPLES:
- "don't you" → /doʊntʃuː/ → "Don-choo"
- "would you" → /wʊdʒuː/ → "Wood-joo"
- "miss you" → /mɪʃuː/ → "Mi-shoo"
- "as you know" → /æʒuː noʊ/ → "A-zhoo know"
- "what did you do?" → /wʌ.dʒə duː/ → "Wha-djuh do?"

MORE: "could you" → "cood-joo", "did you" → "did-joo", "meet you" → "mee-choo",
      "can't you" → "can-choo", "hit you" → "hi-choo", "need you" → "nee-joo",
      "that year" → "tha-cheer", "last year" → "las-cheer", "this year" → "thi-sheer"

Cover ALL 4 fusion types (/tʃ/, /dʒ/, /ʃ/, /ʒ/). Include the interrogative chunk forms.
""",
    },
    6: {
        "name": "Resyllabification",
        "deck": "03_Languages::English::Phonetics::CS_06_Resyllabification",
        "file": "06_Resyllabification.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for C+V Linking / Resyllabification.

RULE: A final consonant migrates to become the onset of the next word's initial vowel,
creating a new syllable boundary. The listener hears ONE flowing long word.

REFERENCE EXAMPLES:
- "check it out" → /tʃɛ.kɪ.taʊt/ → "Che-ki-tout"
- "hold on" → /hoʊl.dɑːn/ → "Hol-don"
- "an apple" → /ə.næ.pəl/ → "A-napple"
- "far away" → /fɑː.rə.weɪ/ → "Fa-ra-way"
- "pick it up" → /pɪ.kɪ.tʌp/ → "Pi-ki-tup"

MORE: "take it easy" → "tay-ki-tee-zy", "give it up" → "gi-vi-tup",
      "work it out" → "wor-ki-tout", "turn it on" → "tur-ni-ton",
      "come on in" → "co-mo-nin", "get in" → "ge-tin", "put it away" → "pu-ti-taway",
      "set it off" → "se-ti-toff", "wrap it up" → "wra-pi-tup"
""",
    },
    7: {
        "name": "H_Dropping",
        "deck": "03_Languages::English::Phonetics::CS_07_H_Dropping",
        "file": "07_H_Dropping.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Weak H-Dropping in function words.

RULE: The /h/ at the start of UNSTRESSED pronouns and auxiliaries vanishes in fast speech:
  him → /ɪm/, her → /ər/, his → /ɪz/, he → /iː/, have → /əv/, had → /əd/, has → /əz/
The pronoun fuses phonetically with the preceding word.

REFERENCE EXAMPLES:
- "tell him" → /tɛl ɪm/ → "Tell-im"
- "what did he say?" → /wʌ.dɪ.di seɪ/ → "Wha-di-dee say?"
- "ask her" → /æs kər/ → "As-ker"
- "I should have known" → /aɪ ʃʊ.də noʊn/ → "I shoulda known"
- "did he leave?" → /dɪ.di liːv/ → "Did-ee leave?"

MORE: "give him a call" → "give-im a call", "I saw her" → "I saw-er",
      "have you?" → "av-you?", "he had it" → "ee-ad-it",
      "tell her everything" → "tell-er everything",
      "what has he done?" → "wha-taz-ee done?"
""",
    },
    8: {
        "name": "Schwa_Reduction",
        "deck": "03_Languages::English::Phonetics::CS_08_Schwa_Reduction",
        "file": "08_Schwa_Reduction.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Schwa /ə/ Reduction (Vowel Reduction).

RULE: Unstressed grammatical/function words lose their full vowel and reduce to schwa /ə/
or near-zero in connected speech. These words become almost INAUDIBLE murmurs.

SCHWA REDUCTION INVENTORY:
  can /kæn/ → /kən/    |  to /tuː/ → /tə/    |  the /ðiː/ → /ðə/
  of /ɒv/ → /əv/       |  for /fɔːr/ → /fər/  |  and /ænd/ → /ən/
  a /eɪ/ → /ə/         |  at /æt/ → /ət/       |  was /wɒz/ → /wəz/
  that /ðæt/ → /ðət/   |  have /hæv/ → /həv/   |  from /frɒm/ → /frəm/
  than /ðæn/ → /ðən/   |  as /æz/ → /əz/       |  but /bʌt/ → /bət/

REFERENCE EXAMPLE:
"I can go to the store for you" → /aɪ kən ɡoʊ tə ðə stɔːr fər juː/
→ "I kn-go tuh-thuh store fer-yuh" (5 reductions in one sentence!)

Generate full sentences showing MAXIMUM schwa density.
In phonetic_breakdown, COUNT how many words reduced and list each one.
TIER 3 cards should have 6+ reduced words per sentence.
""",
    },
    9: {
        "name": "Linking_R",
        "deck": "03_Languages::English::Phonetics::CS_09_Linking_R",
        "file": "09_Linking_R.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Linking R & Intrusive R (British/Australian).

TWO PHENOMENA — mark clearly which type each card demonstrates:

LINKING R: A written 'r' that is normally silent (non-rhotic) gets pronounced when
the NEXT word starts with a vowel.
  "far away" (UK) → /fɑː.rə.weɪ/ → "Far-away" (the r links)
  "four of them" → /fɔː.rəv ðəm/ → "Four-of-them"

INTRUSIVE R: An /r/ is INSERTED between two vowels even when NO 'r' exists in spelling.
  "law and order" → /lɔː.rən.ɔː.də/ → "Law-r-and order"
  "idea of it" → /aɪˈdɪə.rəv.ɪt/ → "Idea-r-of-it"
  "media event" → /ˈmiː.di.ə.rɪ.vɛnt/ → "Media-r-event"

CONTRAST with American rhotic English where R is always pronounced regardless.
Focus on RP British accent. Include Australian examples in Tier 3.
""",
    },
    10: {
        "name": "Lexical_Chunks",
        "deck": "03_Languages::English::Phonetics::CS_10_Lexical_Chunks",
        "file": "10_Lexical_Chunks.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Lexical Compressions (Chunking).

RULE: High-frequency phrase combinations undergo automatic phonetic fusion into a
single acoustic unit. These are fully grammaticalized colloquial reductions.

CHUNK INVENTORY:
  going to   → gonna  /ɡənə/        want to    → wanna  /wɑːnə/
  got to     → gotta  /ɡɑːtə/       have to    → hafta  /ˈhæf.tə/
  ought to   → oughta /ˈɔː.tə/      supposed to→ s'posed/spəʊzd/
  kind of    → kinda  /ˈkaɪn.də/    sort of    → sorta  /ˈsɔːr.tə/
  out of     → outta  /ˈaʊ.tə/      let me     → lemme  /ˈlɛm.i/
  give me    → gimme  /ˈɡɪm.i/      come on    → c'mon  /kəˈmɒn/
  should have→ shoulda/ˈʃʊ.də/      would have → woulda /ˈwʊ.də/
  could have → coulda /ˈkʊ.də/      must have  → musta  /ˈmʌs.tə/
  what are you→whatcha/ˈwʌ.tʃə/     don't know → dunno  /dəˈnoʊ/
  going to be→ gonna be /ˈɡənə biː/

IMPORTANT: Embed each chunk in a natural conversational sentence (not isolated).
Tier 3 cards should chain 2-3 chunks in one sentence: "I'm gonna wanna getta outta here."
""",
    },
    11: {
        "name": "Dark_L",
        "deck": "03_Languages::English::Phonetics::CS_11_Dark_L",
        "file": "11_Dark_L.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Dark L & L-Vocalization.

TWO ALLOPHONES of English /l/:
  CLEAR L [l]: word-initial or before vowels — tongue tip touches alveolar ridge.
    "love", "light", "play" → clear, bright L
  DARK L [ɫ]: after vowels, before consonants, or word-final — tongue body retracts.
    Sounds like a thick "OU/W" vowel. "milk" → "miwk", "feel" → "feew"

L-VOCALIZATION (Cockney, Australian, some AAVE): Dark L becomes full /w/ or /ʊ/:
  "milk" → /mɪʊk/ → "Miwk"
  "feel" → /fiːw/ → "Feew"
  "bottle" → /ˈbɑː.ɾoʊ/ → "Baa-dou"

REFERENCE EXAMPLES:
- "cold" → /koʊd/ → "Cowd"    |  "help" → /hɛwp/ → "Hewp"
- "told" → /toʊd/ → "Towd"   |  "ball" → /bɔːw/ → "Baww"
- "full" → /fʊw/ → "Fuw"     |  "well" → /wɛw/ → "Wew"

Include MINIMAL PAIRS showing Clear L vs Dark L in same word: "lily", "lull", "level"
""",
    },
    12: {
        "name": "Intrusive_Glides",
        "deck": "03_Languages::English::Phonetics::CS_12_Intrusive_Glides",
        "file": "12_Intrusive_Glides.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Intrusive Glides /w/ and /j/.

RULE: To avoid vowel hiatus (two adjacent vowels), English inserts a transitional glide:
  After rounded vowels /uː, oʊ, aʊ/  → insert /w/: "go out" = "go-W-out"
  After front/high vowels /iː, eɪ, aɪ/ → insert /j/: "see it" = "see-Y-it"

TRIGGER MATRIX:
  /uː/ + vowel → /w/: "do it", "who asked", "two options", "through all"
  /oʊ/ + vowel → /w/: "go in", "show off", "slow and", "know about"
  /aʊ/ + vowel → /w/: "how about", "now I", "allow it"
  /iː/ + vowel → /j/: "see it", "free agent", "be aware", "three of"
  /eɪ/ + vowel → /j/: "say it", "pay off", "play it", "way out"
  /aɪ/ + vowel → /j/: "I am", "try it", "by all", "my opinion"

REFERENCE: "go-W-out", "do-W-it", "see-Y-it", "I-Y-am", "two-W-options"

Include examples where the glide is barely perceptible (Tier 1) vs. very noticeable (Tier 3).
""",
    },
    13: {
        "name": "Unreleased_Stops",
        "deck": "03_Languages::English::Phonetics::CS_13_Unreleased_Stops",
        "file": "13_Unreleased_Stops.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Unreleased/Held Stops (Unexploded Plosives).

RULE: Final plosives /p, t, k, b, d, g/ before another consonant are HELD (closure is
made) but NOT released with a burst of air. In IPA: ̚ diacritic marks unreleased stops.
The result: no audible burst — the sound appears to "vanish" between words.

REFERENCE EXAMPLES:
- "stop it" → /stɑːp̚ ɪt/ → The 'p' closes but no air bursts out
- "hot dog" → /hɑːt̚ dɔːɡ/ → The 't' blocks the airflow, then seamlessly into 'd'
- "cat food" → /kæt̚ fuːd/ → The final 't' is swallowed before 'f'
- "big deal" → /bɪɡ̚ diːl/ → The 'g' is held, then straight into 'd'
- "back pack" → /bæk̚ pæk/ → Both K sounds are unreleased

FULL CONSONANT SET: /p̚/ top-down, /t̚/ that day, /k̚/ black coffee,
                    /b̚/ grab that, /d̚/ good morning, /g̚/ big picture

Phonetic_breakdown must explain: "There is NO release burst. The mouth closes and stays
closed. The listener hears a compression or silence, then the next consonant."
""",
    },
    14: {
        "name": "Stress_Timed_Rhythm",
        "deck": "03_Languages::English::Phonetics::CS_14_Stress_Rhythm",
        "file": "14_Stress_Timed_Rhythm.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Stress-Timed Rhythm & Isochrony.

RULE: English is STRESS-TIMED: the interval between STRESSED syllables is approximately
equal, regardless of the number of unstressed syllables between them.
Consequence: sentences with more syllables don't take more time — unstressed syllables
compress to fit the rhythmic grid.

DEMONSTRATION PAIRS (same stress pattern ≈ same duration):
  Simple:   "CATS CHASE MICE"  (~1.5s)
  Complex:  "The CATS have been CHASING all the little MICE" (~1.5s)

EXERCISE FORMAT for each card:
  1. Short version (few syllables, same stress beats)
  2. Long version (many syllables, same stress beats — but same duration!)
  The gap_text should ask: "How long does this take compared to the short version?"

INCLUDE:
  - "Schwa avalanche" examples: long strings of unstressed syllables between beats
  - Contrastive pairs: Spanish syllable-timed vs English stress-timed
  - 3-beat, 4-beat, and 5-beat rhythm frames with variable syllable counts
""",
    },
    15: {
        "name": "Flap_D",
        "deck": "03_Languages::English::Phonetics::CS_15_Flap_D",
        "file": "15_Flap_D.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Flap D (Intervocalic D Flapping).

RULE: In American English, intervocalic /d/ also becomes a flap [ɾ], making some pairs
near-homophones. Both /t/ and /d/ between vowels → [ɾ] → IDENTICAL sound.

HOMOPHONE PAIRS (these sound IDENTICAL in fast American English):
  ladder/latter  → /ˈlæ.ɾər/ both!
  riding/writing → /ˈraɪ.ɾɪŋ/ near-identical
  body/botty     |  medal/metal  |  muddy/muttie
  padding/patting | heading/hating | loading/noting

KEY INSIGHT FOR LEARNERS: Context disambiguates! Native speakers don't hear them
differently — the surrounding words clarify meaning.

CROSS-WORD BOUNDARY EXAMPLES:
  "made an offer" → "may-dan offer"  (d becomes flap before unstressed vowel)
  "hide it" → "hi-did" (the d at the end flaps before 'it')
  "she'd asked" → "shee-dasked"

Generate cards that highlight the PERCEPTUAL AMBIGUITY these create, 
showing how context resolves them.
""",
    },
    16: {
        "name": "Pre_Glottalization",
        "deck": "03_Languages::English::Phonetics::CS_16_Pre_Glottalization",
        "file": "16_Pre_Glottalization.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Pre-Glottalization (Glottal Reinforcement).

RULE: Before voiceless plosives /p, t, k/ at certain syllable boundaries, a SIMULTANEOUS
glottal closure [ʔ] is added alongside (NOT instead of) the oral stop.
This creates an audible "dry knock" in the throat before the consonant.

DISTINCTION FROM GLOTTAL STOP (Rule 3):
  Glottal stop REPLACES /t/ (Rule 3): "butter" → "bu'er" (no tongue contact)
  Pre-glottalization REINFORCES /p,t,k/: "napkin" → /ˈnæʔp.kɪn/ (glottal + lip closure)

REFERENCE EXAMPLES:
- "napkin" → /ˈnæʔp.kɪn/    |   "actor" → /ˈæʔk.tər/
- "backward" → /ˈbæʔk.wərd/ |   "apt" → /æʔpt/
- "captain" → /ˈkæʔp.tɪn/   |   "doctor" → /ˈdɒʔk.tər/
- "sector" → /ˈsɛʔk.tər/    |   "aspect" → /ˈæʔs.pɛkt/

COMMON ENVIRONMENTS: -pt-, -kt-, -pk-, -pk- clusters, before syllable-boundary stops
Phonetic_breakdown must note: "Both the throat AND the lips/tongue close simultaneously."
""",
    },
    17: {
        "name": "Auxiliary_Chunks",
        "deck": "03_Languages::English::Phonetics::CS_17_Auxiliary_Chunks",
        "file": "17_Auxiliary_Chunks.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Advanced Auxiliary Chunks.

RULE: Entire question/modal structures undergo SIMULTANEOUS application of:
  - Yod coalescence (/d/+/j/ → /dʒ/)
  - H-dropping (pronoun 'h' disappears)
  - Schwa reduction (auxiliary vowels collapse)
  - Lexical compression (sequence fuses into one acoustic unit)

REFERENCE EXAMPLES (show the MULTI-RULE cascade):
  "What did you do?" → /wʌ.dʒə duː/ → "Whadja do?"
    [cluster elision + yod coalescence + schwa]
  "Did you ever...?" → /ˈdʒɛ.vər/ → "Jever...?"
    [yod coalescence + H-drop + schwa compression → 2 syllables!]
  "Would have been" → /wʊ.də bɪn/ → "Woulda bin"
    [schwa + lexical chunk]
  "What do you mean?" → /wʌ.də.jə miːn/ → "Whadaya mean?"
  "Do you know what I mean?" → /jə noʊ wʌ.daɪ miːn/ → "Ya know whad-I mean?"
  "I don't know what you're talking about" → "I dunno whacha talkin' 'bout"

Tier 3 should include full colloquial exchanges (A: "Whadja do?" B: "Dunno, jus' hung out")
""",
    },
    18: {
        "name": "Syllabic_Consonants",
        "deck": "03_Languages::English::Phonetics::CS_18_Syllabic_Consonants",
        "file": "18_Syllabic_Consonants.json",
        "template": "T9_ListeningChunk",
        "system_prompt": BASE_SYSTEM_PROMPT,
        "user_prompt": """\
Generate {count} T9_ListeningChunk cards for Syllabic Consonants.

RULE: The vowel in an unstressed syllable is DELETED entirely, leaving the consonant
(/n/, /l/, /m/, /r/) to function as the syllable NUCLEUS — its own beat with no vowel.
In IPA, syllabic consonants are marked with a vertical tick: n̩, l̩, m̩, r̩.

REFERENCE EXAMPLES:
- "sudden" → /ˈsʌd.n̩/ → "Sudd-n" (the /ə/ is gone; /n̩/ is the syllable)
- "rhythm"  → /ˈrɪð.m̩/ → "Rhyth-m"
- "little"  → /ˈlɪ.ɾl̩/ → "Litt-l"
- "bottle"  → /ˈbɑ.ɾl̩/ → "Bott-l"
- "button"  → /ˈbʌ.ʔn̩/ → "Butt-n" (glottal + syllabic N)
- "garden"  → /ˈɡɑːd.n̩/ → "Gard-n"
- "prison"  → /ˈprɪz.n̩/ → "Priz-n"
- "national" → /ˈnæʃ.n̩l̩/ → "Nash-nl"

MORE: cotton/cott-n, kitten/kitt-n, fatten/fatt-n, bitten/bitt-n,
      middle/midd-l, table/tayb-l, apple/app-l, simple/simpl,
      channel/chann-l, tunnel/tunn-l, symbol/symb-l, rhythm/rhyth-m

IMPORTANT: The phonetic_breakdown must specify which consonant is syllabic and why
the vowel deletion occurs (unstressed position + following sonorant).
""",
    },
}


# ============================================================
# CARD RENDERING — Convert generator output → AnkiConnect format
# ============================================================

AUDIO_BUTTON_STYLE = (
    "background:{bg};color:white;padding:5px 11px;border-radius:5px;"
    "text-decoration:none;font-size:0.88em;font-family:sans-serif;"
    "display:inline-block;margin:2px;"
)
PHONEME_HIGHLIGHT = "color:#FF6B35;font-weight:bold;"
TRANSCRIPT_BOX = (
    "background:#FFF8E7;border-left:3px solid #FF6B35;padding:6px 10px;"
    "border-radius:4px;font-family:monospace;margin:6px 0;"
)


def make_audio_buttons(youglish: str, forvo: str) -> str:
    """Renders HTML audio button row for the card front."""
    yt_btn = (
        f'<a href="{youglish}" target="_blank" '
        f'style="{AUDIO_BUTTON_STYLE.format(bg="#2E7D32")}">🎧 YouGlish</a>'
    ) if youglish else ""
    fv_btn = (
        f'<a href="{forvo}" target="_blank" '
        f'style="{AUDIO_BUTTON_STYLE.format(bg="#1565C0")}">🔊 Forvo</a>'
    ) if forvo else ""
    return f'<div style="margin-bottom:10px">{yt_btn}&nbsp;{fv_btn}</div>'


def render_t9_card(raw: Dict[str, Any], rule_info: Dict[str, Any]) -> Dict[str, Any]:
    """Converts generator output (T9 raw) into AnkiConnect-ready card dict."""
    phrase = raw.get("full_transcript", "")
    forvo_word = raw.get("audio_search_forvo", phrase.split()[0] if phrase else "")
    yg_phrase = raw.get("audio_search_youglish", phrase[:50])

    yt_url = youglish_url(yg_phrase, "en", "us")
    fv_url = forvo_url(forvo_word, "en")
    audio_buttons = make_audio_buttons(yt_url, fv_url)

    rules = raw.get("rules_applied", [])
    rules_html = "".join(f"<li><code>{r}</code></li>" for r in rules)

    connected = raw.get("connected_form", "")
    ipa = raw.get("ipa_transcription", "")
    breakdown = raw.get("phonetic_breakdown", "")
    tier = raw.get("tier", 1)
    gap = raw.get("gap_text", f"{{{{c1::{connected}}}}}")

    return {
        "deck": rule_info["deck"],
        "scenario": raw.get("scenario", f"Fast English: {rule_info['name']} 🎧 — Tier {tier}"),
        "text": (
            f"{audio_buttons}"
            f"<b>Fill the gap:</b><br>{gap}"
        ),
        "explanation": (
            f"<b>Written:</b> {phrase}<br>"
            f"<b>Native speed:</b> "
            f'<span style="{TRANSCRIPT_BOX}">'
            f'<span style="{PHONEME_HIGHLIGHT}">{connected}</span></span><br>'
            f"<b>IPA:</b> <code>{ipa}</code><br><br>"
            f"<b>Rules applied:</b><ul>{rules_html}</ul>"
            f"<br>🧠 <b>Phonetics:</b> {breakdown}"
        ),
        "usage": (
            f"Written: <code>{phrase}</code><br>"
            f'Native: <span style="{PHONEME_HIGHLIGHT}">{connected}</span><br>'
            f"IPA: <code>{ipa}</code><br>"
            f"{audio_buttons}"
        ),
        "spanish": raw.get("spanish", f"Pronunciación conectada: {connected}"),
        "audio_links": {"youglish_phrase": yt_url, "forvo_word": fv_url},
        "tags": (
            ["english", "phonetics", "connected_speech",
             rule_info["name"].lower(), f"tier_{tier}"]
            + [r.lower().replace(" ", "_").replace("/", "") for r in rules[:3]]
        ),
    }


def render_t8_card(raw: Dict[str, Any], rule_info: Dict[str, Any]) -> Dict[str, Any]:
    """Converts generator output (T8 raw) into AnkiConnect-ready card dict."""
    pa = raw.get("phoneme_a", "/ɪ/")
    pb = raw.get("phoneme_b", "/iː/")
    ipa_a = raw.get("ipa_a", "")
    ipa_b = raw.get("ipa_b", "")
    pairs = raw.get("word_pairs", [])
    muscle = raw.get("muscle_tip", "")

    fv_a = forvo_url(raw.get("audio_search_phoneme_a", pairs[0][0] if pairs else ""), "en")
    fv_b = forvo_url(raw.get("audio_search_phoneme_b", pairs[0][1] if pairs else ""), "en")
    ipa_ref = ipa_chart_url(pa)

    pairs_rows = "".join(
        f"<tr>"
        f"<td><a href='{fv_a}' target='_blank'>🔊</a> <b>{p[0]}</b></td>"
        f"<td><code>{p[2] if len(p) > 2 else ''}</code></td>"
        f"<td><b>{p[1]}</b></td>"
        f"<td><code>{p[3] if len(p) > 3 else ''}</code></td>"
        f"</tr>"
        for p in pairs
    )
    table = (
        "<table border='1' cellpadding='5' style='border-collapse:collapse;width:100%'>"
        "<thead style='background:#E3F2FD'><tr>"
        f"<th>Word A ({pa})</th><th>IPA A</th>"
        f"<th>Word B ({pb})</th><th>IPA B</th>"
        "</tr></thead>"
        f"<tbody>{pairs_rows}</tbody></table>"
    )

    color_a = "#1565C0"
    color_b = "#4CAF50"
    color_ref = "#6A1B9A"
    
    return {
        "deck": rule_info["deck"],
        "scenario": f"Minimal Pair 🎯: {pa} vs {pb} (EN)",
        "text": (
            f"<div style='margin-bottom:10px'>"
            f"<a href='{fv_a}' target='_blank' style='{AUDIO_BUTTON_STYLE.format(bg=color_a)}'>🔊 {pa}</a>&nbsp;"
            f"<a href='{fv_b}' target='_blank' style='{AUDIO_BUTTON_STYLE.format(bg=color_b)}'>🔊 {pb}</a>&nbsp;"
            f"<a href='{ipa_ref}' target='_blank' style='{AUDIO_BUTTON_STYLE.format(bg=color_ref)}'>📖 IPAchart</a>"
            f"</div>"
            f"<b>Phoneme A</b> <code>{pa}</code><br>"
            f"<b>IPA description:</b> {{{{c1::{ipa_a}}}}}"
        ),
        "explanation": (
            f"<b>{pa}</b> — {ipa_a}<br>"
            f"<b>{pb}</b> — {ipa_b}<br><br>"
            f"<b>🧠 Articulatory Tip (ES):</b> {muscle}<br><br>"
            f"{table}"
        ),
        "usage": table,
        "spanish": muscle,
        "audio_links": {
            "phoneme_a": fv_a, "phoneme_b": fv_b,
            "ipa_chart": ipa_ref,
        },
        "tags": ["english", "phonetics", "minimal_pair",
                 pa.strip("/[]").replace("ː", "_long"),
                 pb.strip("/[]").replace("ː", "_long")],
    }


# ============================================================
# GEMINI API CALL
# ============================================================

def call_gemini(system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
    """Calls Gemini API with retry + exponential backoff."""
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": f"{system_prompt}\n\n---\n\n{user_prompt}"}],
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2,
            "maxOutputTokens": 8192,
        },
    }
    headers = {"Content-Type": "application/json"}

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            content = result["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(content)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait = RETRY_BACKOFF * (2 ** attempt)
                print(f"    [!] Rate limited. Waiting {wait:.1f}s...")
                time.sleep(wait)
            else:
                print(f"    [-] HTTP {e.response.status_code}: {e}")
                return None
        except Exception as e:
            print(f"    [-] Error (attempt {attempt+1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFF)
    return None


# ============================================================
# MAIN GENERATOR LOGIC
# ============================================================

def generate_rule(
    rule_num: int,
    count: int = 15,
    dry_run: bool = False,
    append: bool = False,
) -> bool:
    """Generates cards for one phonetic rule and saves to deck JSON file.

    Args:
        rule_num: Rule number from RULE_CATALOG (0-18).
        count: Number of cards to generate.
        dry_run: Print prompt without calling API.
        append: Append to existing file instead of overwriting.

    Returns:
        True if successful.
    """
    if rule_num not in RULE_CATALOG:
        print(f"[-] Unknown rule number: {rule_num}. Use --list to see options.")
        return False

    info = RULE_CATALOG[rule_num]
    template = info["template"]
    system_prompt = info["system_prompt"]
    user_prompt = info["user_prompt"].format(count=count)

    print(f"\n[→] Rule {rule_num:02d}: {info['name']} ({template})")
    print(f"    Deck: {info['deck']}")
    print(f"    File: {info['file']}")

    if dry_run:
        print("\n=== SYSTEM PROMPT ===")
        print(system_prompt[:500] + "...")
        print("\n=== USER PROMPT ===")
        print(user_prompt)
        return True

    if not GEMINI_API_KEY:
        print("[-] GEMINI_API_KEY not set. Run: set GEMINI_API_KEY=your_key")
        return False

    print(f"    Generating {count} cards via Gemini API...")
    response = call_gemini(system_prompt, user_prompt)

    if not response:
        print(f"    [-] Generation failed for rule {rule_num}.")
        return False

    raw_cards = response.get("cards", [])
    print(f"    [+] Received {len(raw_cards)} raw cards from Gemini.")

    # Render to AnkiConnect format
    rendered = []
    for raw in raw_cards:
        try:
            if template == "T8_MinimalPair":
                card = render_t8_card(raw, info)
            else:
                card = render_t9_card(raw, info)

            # Run validator pipeline
            _, cleaned, errs = sanitize_and_validate_card(card)
            if errs:
                print(f"    [!] Validator warnings: {errs[:2]}")
            rendered.append(cleaned)
        except Exception as e:
            print(f"    [!] Card rendering error: {e}")

    print(f"    [✓] {len(rendered)} cards rendered and validated.")

    # Save to deck file (UTF-8 explicit per Q3)
    DECKS_PHONETICS.mkdir(parents=True, exist_ok=True)
    out_file = DECKS_PHONETICS / info["file"]

    existing = []
    if append and out_file.exists():
        with open(out_file, "r", encoding="utf-8") as f:
            existing = json.load(f)
        print(f"    [+] Appending to {len(existing)} existing cards.")

    all_cards = existing + rendered
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_cards, f, indent=2, ensure_ascii=False)

    print(f"    [✓] Saved {len(all_cards)} cards → {out_file}")
    return True


# ============================================================
# CLI
# ============================================================

def cmd_list() -> None:
    """Prints the rule catalog."""
    print("\n=== PHONETICS RULE CATALOG ===")
    print(f"{'#':<4} {'Name':<28} {'Template':<22} {'Output File'}")
    print("-" * 75)
    for num, info in RULE_CATALOG.items():
        print(f"{num:<4} {info['name']:<28} {info['template']:<22} {info['file']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Phonetics Corpus Generator — LLM-Orchestrated Anki Card Factory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--rule", type=int, default=None, help="Rule number (0-18)")
    parser.add_argument("--all", action="store_true", help="Generate all 18 rules")
    parser.add_argument("--count", type=int, default=15, help="Cards per rule (default: 15)")
    parser.add_argument("--dry-run", action="store_true", help="Show prompt, no API call")
    parser.add_argument("--append", action="store_true", help="Append to existing file")
    parser.add_argument("--list", action="store_true", help="Show rule catalog and exit")
    args = parser.parse_args()

    if args.list:
        cmd_list()
        return

    if args.all:
        print(f"[+] Generating ALL {len(RULE_CATALOG)} rules × {args.count} cards each.")
        success = 0
        for rule_num in sorted(RULE_CATALOG.keys()):
            if generate_rule(rule_num, args.count, args.dry_run, args.append):
                success += 1
            time.sleep(2)  # Rate limiting between rules
        print(f"\n[✓] Completed: {success}/{len(RULE_CATALOG)} rules generated.")
        return

    if args.rule is None:
        parser.print_help()
        return

    generate_rule(args.rule, args.count, args.dry_run, args.append)


if __name__ == "__main__":
    main()
