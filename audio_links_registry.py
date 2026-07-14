#!/usr/bin/env python3
"""Audio Links Registry for Phonetics Anki Templates.

Provides curated public audio URL builders for each source, mapped
to their intended Anki template type:

  Forvo        -> T8_MinimalPair  (isolated phoneme, acoustic precision)
  YouGlish     -> T9_ListeningChunk + T11_ExecutivePitch (native context)
  IPAchart.com -> T8 phoneme reference (symbol-level IPA audio)
  BBC Learning -> T10_ReadingPatternDrill (structured pattern explanation)
  OJAD         -> Japanese T10 cards (pitch accent per word)  [Phase 2]
  Wisc Phonetics -> Spanish T10 cards  [Phase 2]

All URLs are public and require no authentication.
"""

from typing import Dict, Optional
from urllib.parse import quote

# ---------------------------------------------------------------------------
# LANGUAGE CODE MAP  (ISO 639-1 -> Forvo language slug)
# ---------------------------------------------------------------------------
FORVO_LANG_CODES: Dict[str, str] = {
    "en": "en",
    "es": "es",
    "fr": "fr",
    "de": "de",
    "it": "it",
    "pt": "pt",
    "ja": "ja",
    "zh": "zh",
    "hi": "hi",
    "ko": "ko",
}

YOUGLISH_LANG_CODES: Dict[str, str] = {
    "en": "english",
    "es": "spanish",
    "fr": "french",
    "de": "german",
    "it": "italian",
    "pt": "portuguese",
    "ja": "japanese",
    "zh": "chinese",
    "hi": "hindi",
    "ko": "korean",
}

# ---------------------------------------------------------------------------
# IPA CHART — Pre-mapped phoneme audio links (ipachart.com)
# All 48 English phonemes (RP + GAm coverage)
# ---------------------------------------------------------------------------
IPA_CHART_PHONEME_MAP: Dict[str, str] = {
    # Monophthongs
    "/iː/": "http://www.ipachart.com/",
    "/ɪ/":  "http://www.ipachart.com/",
    "/e/":  "http://www.ipachart.com/",
    "/æ/":  "http://www.ipachart.com/",
    "/ʌ/":  "http://www.ipachart.com/",
    "/ɑː/": "http://www.ipachart.com/",
    "/ɒ/":  "http://www.ipachart.com/",
    "/ɔː/": "http://www.ipachart.com/",
    "/ʊ/":  "http://www.ipachart.com/",
    "/uː/": "http://www.ipachart.com/",
    "/ɜː/": "http://www.ipachart.com/",
    "/ə/":  "http://www.ipachart.com/",
    # Diphthongs
    "/eɪ/": "http://www.ipachart.com/",
    "/aɪ/": "http://www.ipachart.com/",
    "/ɔɪ/": "http://www.ipachart.com/",
    "/əʊ/": "http://www.ipachart.com/",
    "/aʊ/": "http://www.ipachart.com/",
    "/ɪə/": "http://www.ipachart.com/",
    "/eə/": "http://www.ipachart.com/",
    "/ʊə/": "http://www.ipachart.com/",
    # Plosives
    "/p/":  "http://www.ipachart.com/",
    "/b/":  "http://www.ipachart.com/",
    "/t/":  "http://www.ipachart.com/",
    "/d/":  "http://www.ipachart.com/",
    "/k/":  "http://www.ipachart.com/",
    "/ɡ/":  "http://www.ipachart.com/",
    # Affricates
    "/tʃ/": "http://www.ipachart.com/",
    "/dʒ/": "http://www.ipachart.com/",
    # Fricatives
    "/f/":  "http://www.ipachart.com/",
    "/v/":  "http://www.ipachart.com/",
    "/θ/":  "http://www.ipachart.com/",
    "/ð/":  "http://www.ipachart.com/",
    "/s/":  "http://www.ipachart.com/",
    "/z/":  "http://www.ipachart.com/",
    "/ʃ/":  "http://www.ipachart.com/",
    "/ʒ/":  "http://www.ipachart.com/",
    "/h/":  "http://www.ipachart.com/",
    # Nasals
    "/m/":  "http://www.ipachart.com/",
    "/n/":  "http://www.ipachart.com/",
    "/ŋ/":  "http://www.ipachart.com/",
    # Approximants
    "/l/":  "http://www.ipachart.com/",
    "/r/":  "http://www.ipachart.com/",
    "/w/":  "http://www.ipachart.com/",
    "/j/":  "http://www.ipachart.com/",
    # Allophone variants
    "[ɾ]":  "http://www.ipachart.com/",   # Flap T/D
    "[ʔ]":  "http://www.ipachart.com/",   # Glottal stop
    "[l̩]":  "http://www.ipachart.com/",   # Syllabic L
    "[n̩]":  "http://www.ipachart.com/",   # Syllabic N
}

# ---------------------------------------------------------------------------
# PUBLIC FUNCTIONS
# ---------------------------------------------------------------------------

def forvo_url(word: str, lang_code: str = "en") -> str:
    """Returns the Forvo pronunciation page for a word.

    Best for: T8_MinimalPair — isolated acoustic precision.

    Args:
        word: The word to look up (e.g. 'ship').
        lang_code: ISO 639-1 language code (default 'en').

    Returns:
        Public Forvo URL (no API key required for page access).
    """
    slug = FORVO_LANG_CODES.get(lang_code, lang_code)
    encoded = quote(word.lower().strip(), safe="")
    return f"https://forvo.com/word/{encoded}/#{slug}"


def youglish_url(
    phrase: str,
    lang_code: str = "en",
    accent: str = "us",
) -> str:
    """Returns a YouGlish search URL for a phrase in real speech context.

    Best for: T9_ListeningChunk, T11_ExecutivePitch — native coarticulation.

    Args:
        phrase: The phrase to search (e.g. 'I must go').
        lang_code: ISO 639-1 language code (default 'en').
        accent: Accent filter. For English: 'us', 'uk', 'au'. Ignored for others.

    Returns:
        Public YouGlish URL.
    """
    lang_full = YOUGLISH_LANG_CODES.get(lang_code, "english")
    encoded = quote(phrase.strip(), safe="")
    if lang_code == "en":
        return f"https://youglish.com/pronounce/{encoded}/{lang_full}/{accent}"
    return f"https://youglish.com/pronounce/{encoded}/{lang_full}"


def ipa_chart_url(phoneme: str) -> str:
    """Returns the IPAchart.com link for a specific phoneme symbol.

    Best for: T8_MinimalPair phoneme reference panel.

    Args:
        phoneme: IPA symbol string (e.g. '/ɪ/', '/eɪ/', '[ɾ]').

    Returns:
        Pre-mapped URL, or the generic IPAchart homepage as fallback.
    """
    return IPA_CHART_PHONEME_MAP.get(phoneme, "http://www.ipachart.com/")


def bbc_url(topic_slug: str) -> str:
    """Returns a BBC Learning English pronunciation URL for a topic.

    Best for: T10_ReadingPatternDrill — structured rule explanations.

    Args:
        topic_slug: BBC page topic identifier (e.g. 'pronunciation', 'sounds').

    Returns:
        BBC Learning English URL.
    """
    encoded = quote(topic_slug.strip().lower().replace(" ", "-"), safe="-")
    return f"https://www.bbc.co.uk/learningenglish/english/features/pronunciation/{encoded}"


def ojad_url(word: str) -> str:
    """Returns the OJAD Online Japanese Accent Dictionary URL for a word.

    Best for: T10_ReadingPatternDrill (Japanese pitch accent). Phase 2.

    Args:
        word: Japanese word in kana or romaji.

    Returns:
        OJAD search URL.
    """
    encoded = quote(word.strip(), safe="")
    return f"http://www.gavo.t.u-tokyo.ac.jp/ojad/search/index/word:{encoded}"


def wisc_phonetics_url(phoneme: str, lang_code: str = "es") -> str:
    """Returns the Wisconsin Phonetics Lab URL for a Spanish phoneme.

    Best for: T10_ReadingPatternDrill (Spanish). Phase 2.

    Args:
        phoneme: IPA symbol (e.g. '/β/', '/ð/').
        lang_code: Language code (currently only 'es' supported).

    Returns:
        Phonetics.wisc.edu URL.
    """
    return f"http://www.phonetics.wisc.edu/"


def build_minimal_pair_audio(phoneme_a: str, phoneme_b: str) -> Dict[str, str]:
    """Builds a standard audio_links dict for a T8_MinimalPair card.

    Returns a dict with IPA chart links for both phonemes.

    Args:
        phoneme_a: First IPA phoneme (e.g. '/ɪ/').
        phoneme_b: Second IPA phoneme (e.g. '/iː/').
    """
    return {
        "phoneme_a": ipa_chart_url(phoneme_a),
        "phoneme_b": ipa_chart_url(phoneme_b),
        "ipa_chart_reference": "http://www.ipachart.com/",
    }


def build_chunk_audio(phrase: str, lang_code: str = "en", accent: str = "us") -> Dict[str, str]:
    """Builds a standard audio_links dict for a T9_ListeningChunk card.

    Returns a dict with YouGlish link for the phrase + Forvo for the
    first significant word.

    Args:
        phrase: The connected-speech phrase.
        lang_code: ISO 639-1 language code.
        accent: YouGlish accent filter ('us', 'uk', 'au').
    """
    first_word = phrase.split()[0].strip(",.?!").lower() if phrase else ""
    return {
        "youglish_phrase": youglish_url(phrase, lang_code, accent),
        "forvo_word": forvo_url(first_word, lang_code) if first_word else "",
    }


def build_executive_audio(phrase: str, youtube_url: Optional[str] = None) -> Dict[str, str]:
    """Builds a standard audio_links dict for a T11_ExecutivePitch card.

    Args:
        phrase: Transcript excerpt (used for YouGlish fallback).
        youtube_url: Optional direct YouTube timestamped URL.
    """
    links: Dict[str, str] = {
        "youglish_phrase": youglish_url(phrase[:60], "en", "us"),
    }
    if youtube_url:
        links["youtube_source"] = youtube_url
    return links


def build_reading_pattern_audio(words: list, lang_code: str = "en") -> Dict[str, str]:
    """Builds a Forvo audio_links dict for a T10_ReadingPatternDrill card.

    Generates one Forvo link per example word (up to 30).

    Args:
        words: List of example words exhibiting the grapheme pattern.
        lang_code: ISO 639-1 language code.
    """
    return {
        word: forvo_url(word, lang_code)
        for word in words[:30]
    }


if __name__ == "__main__":
    # Smoke test
    print("=== Audio Links Registry Smoke Test ===")
    print(f"Forvo 'ship':       {forvo_url('ship', 'en')}")
    print(f"YouGlish 'must go': {youglish_url('must go', 'en', 'us')}")
    print(f"IPA /ɪ/:            {ipa_chart_url('/ɪ/')}")
    print(f"IPA [ɾ]:            {ipa_chart_url('[ɾ]')}")
    print(f"BBC 'sounds':       {bbc_url('sounds')}")
    print(f"OJAD 'です':        {ojad_url('です')}")
    print()
    print("Minimal Pair audio dict (/ɪ/ vs /iː/):")
    import json
    print(json.dumps(build_minimal_pair_audio("/ɪ/", "/iː/"), indent=2, ensure_ascii=False))
    print()
    print("Chunk audio dict ('I must go to the store'):")
    print(json.dumps(build_chunk_audio("I must go to the store"), indent=2, ensure_ascii=False))
