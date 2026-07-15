#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.append(str(BASE_DIR))

from card_validator import sanitize_and_validate_card

DECK_FILE = BASE_DIR / "decks/03_Languages/Japanese/A1_Beginner/greetings_pronouns_and_verbs.json"

ENRICHED_EXPLANATIONS = {
    "ae78796f8aa1681c": (
        "This is the formal morning greeting. It is derived from the adjective "
        "<b>早い</b> (<i>hayai</i>, meaning 'early'). The prefix <b>お</b> (<i>o-</i>) "
        "and suffix <b>ございます</b> (<i>gozaimasu</i>) elevate the phrase to polite speech (Keigo). "
        "For friends and family, the shortened informal <b>おはよう</b> (<i>Ohayō</i>) is used.<br><br>"
        "🧠 <b>Mnemonic Scene:</b> Imagine waking up early to find a giant glowing <b>O-HAY</b> stack "
        "(Ohayō) sitting in a formal courtroom in front of a judge."
    ),
    "6f3e683572f1c8f6": (
        "Used as a general 'Hello' from late morning through afternoon. Historically, it was the "
        "start of a topic clause: <i>Kon-nichi wa...</i> (Today is...), where <b>wa</b> was followed "
        "by a wish. This is why the final sound is written with the hiragana particle <b>は</b> (<i>ha</i>) "
        "instead of <b>わ</b> (<i>wa</i>).<br><br>"
        "🧠 <b>Mnemonic Scene:</b> A huge clock pointing to <b>noon (nichi)</b> on a giant "
        "<b>cone (kon)</b>, greeting everyone who passes by."
    ),
    "d2e4e2c6f36df30a": (
        "Used as a greeting when meeting someone in the evening. Similar to <i>Konnichiwa</i>, it was "
        "originally a topic clause: <i>Kon-ban wa...</i> (This evening is...), which is why the topic "
        "marker particle <b>は</b> (<i>ha</i>) is used to write the final 'wa' sound.<br><br>"
        "🧠 <b>Mnemonic Scene:</b> A giant <b>cone (kon)</b> holding a <b>banjo (ban)</b> under the starry "
        "evening sky, playing night tunes."
    ),
    "db4ffd9bbcffcf4d": (
        "A formal farewell that carries weight. It implies a long separation, similar to 'Farewell' or "
        "'Adieu' in English, and is generally avoided in daily workplaces because it can sound like you "
        "won't see each other again. With classmates or coworkers, use informal parting phrases like "
        "<i>mata ne</i> or <i>jā ne</i>.<br><br>"
        "🧠 <b>Mnemonic Scene:</b> A traveler waving goodbye from a ship, throwing a giant <b>SA-YO-NARA</b> "
        "banner into the ocean."
    ),
    "34079e03bcfb8acd": (
        "Derived from the verb <b>始める</b> (<i>hajimeru</i>, meaning 'to begin' or 'to start'). "
        "It literally means 'it is beginning [for the first time]'. It is used strictly at the very "
        "beginning of a self-introduction when meeting someone for the first time.<br><br>"
        "🧠 <b>Mnemonic Scene:</b> Two runners at the <b>start line (hajime)</b> of a race, shaking "
        "hands and saying 'Nice to meet you' before the whistle blows."
    ),
    "477113ce487d8958": (
        "Used when parting in the late evening or when going to bed. Derived from the verb <b>休む</b> "
        "(<i>yasumu</i>, meaning 'to rest' or 'to take a break'). The polite form adds the suffix "
        "<b>なさい</b> (<i>nasai</i>). For close friends and family, the casual <b>おやすみ</b> (<i>Oyasumi</i>) "
        "is standard.<br><br>"
        "🧠 <b>Mnemonic Scene:</b> A sleepy person resting in an <b>O-YASU (oasis)</b> at night, counting "
        "sheep that whisper 'nasai'."
    ),
    "92c690ee05d6c69a": (
        "An extremely common, casual parting greeting used among close friends, family, and peers. "
        "<b>じゃあ</b> (<i>Jā</i>) is a contraction of <i>dewa</i> (well then), and <b>ね</b> (<i>ne</i>) is "
        "a friendly confirmation particle (like 'right?' or 'okay?').<br><br>"
        "🧠 <b>Mnemonic Scene:</b> Friends waving goodbye near a giant glass <b>JAR (jā)</b> filled with "
        "friendly smiley faces."
    ),
    "af4b8f7eeb700fc0": (
        "This card emphasizes the spelling of the greeting. Although pronounced as 'wa', the final character "
        "is written using <b>は</b> (<i>ha</i>) because it acts as the grammatical topic marker particle. "
        "This stems from the phrase's historical origin as the beginning of a longer sentence: "
        "<i>Kon-nichi wa [gokigen ikaga desu ka]</i> (How are you doing today?)."
    ),
    "b6689ea6db91f9ad": (
        "Represents the polite greeting used in the morning. In Japanese business culture, "
        "<i>Ohayou gozaimasu</i> is also used as the first greeting of the day when starting a shift, "
        "regardless of the actual time (even in the afternoon or night!)."
    ),
    "2a5defedade7dabc": (
        "In this evening greeting, the final sound 'wa' is written as <b>は</b> (<i>ha</i>) because it was "
        "originally the topic particle in the clause: <i>Kon-ban wa [ikaga osugoshi desu ka]</i> "
        "(How is this evening treating you?). <b>今晩</b> (<i>konban</i>) means 'this evening' (今 = this, 晩 = evening)."
    ),
    "d26e280d5c65c19b": (
        "Formed by the prefix <b>お</b> (honorific), <b>休み</b> (<i>yasumi</i>, rest/break), and <b>なさい</b> "
        "(polite command form). It literally translates to 'Please rest well'. Use <b>おやすみ</b> (<i>Oyasumi</i>) "
        "for children, peers, or family."
    ),
    "308e524f90483439": (
        "Historically derived from the phrase <b>左様ならば</b> (<i>sayō naraba</i>, meaning 'if that is the case' "
        "or 'well then'). Over time, it became a standardized farewell. In daily contexts, it is best to use "
        "<b>お疲れ様でした</b> (<i>Otsukaresama deshita</i>, thank you for your hard work) with coworkers."
    ),
    "d4d9421cb0c0c471": (
        "Derived from <b>始めまして</b> (from <i>hajimeru</i> - to begin). It signals that a new relationship is "
        "starting. Cultural note: It is always accompanied by a bow in Japan to show respect to the new acquaintance."
    ),
    "b80a427e3d148530": (
        "A complex untranslatable phrase. <b>どうぞ</b> (<i>douzo</i>) means 'please/here you go', <b>よろしく</b> "
        "(<i>yoroshiku</i>) comes from <i>yoi</i> (good/favorable), and <b>お願いします</b> (<i>onegaishimasu</i>) "
        "means 'I make a request'. It literally means 'Please treat me favorably hereafter'."
    ),
    "78d74425bc1c8baf": (
        "Difference in requests: <b>お願いします</b> (<i>Onegaishimasu</i>) is 'I pray/beg you' (comes from <i>negau</i> "
        "- to pray/request). <b>ください</b> (<i>Kudasai</i>) is 'give me' (polite form of <i>kudaru</i> - to hand down). "
        "You can say <i>Onegaishimasu</i> to order something in a restaurant or ask for help, but <i>Kudasai</i> "
        "is more transactional (e.g. 'Coffee, please' -> <i>kōhī kudasai</i>)."
    )
}

def main():
    print(f"Loading {DECK_FILE}...")
    with open(DECK_FILE, "r", encoding="utf-8") as f:
        cards = json.load(f)
        
    enriched_count = 0
    for card in cards:
        card_id = card.get("id")
        if card_id in ENRICHED_EXPLANATIONS:
            print(f"Enriching card ID: {card_id}...")
            card["content"]["explanation"] = ENRICHED_EXPLANATIONS[card_id]
            
            # Validate card
            is_valid, cleaned_card, val_errors = sanitize_and_validate_card(card)
            if val_errors:
                print(f"Validation Warning for card {card_id}: {val_errors}")
                
            # Replace card in-memory
            card.clear()
            card.update(cleaned_card)
            enriched_count += 1
            
    print(f"Saving {enriched_count} enriched cards back to {DECK_FILE.name}...")
    with open(DECK_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)
        
    print("[SUCCESS] Direct enrichment complete!")

if __name__ == "__main__":
    main()
