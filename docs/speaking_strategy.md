# Speaking practice strategy

## Goal
Keep the current Anki content system fast and lightweight while adding a speaking workflow that is useful in practice.

## Strategy
1. Keep audio as remote URLs by default.
   - This avoids heavy local media downloads.
   - Cards can play audio directly from the web when available.
2. Use a companion recorder for self-practice.
   - A browser-based recorder allows recording and saving audio locally.
   - It can be opened from Anki cards through a link.
3. Separate speaking practice from the default cloze flow.
   - Speaking practice uses a dedicated Anki model with prompt, audio, and recorder link fields.
   - The main deck remains clean and reusable.
4. Scale gradually.
   - First: prompt + reference audio + recorder.
   - Next: optional pronunciation score or word-level feedback.
   - Later: offline media packs for the most-used cards.

## Current implementation
- Speaker cards are generated with a dedicated template and model support.
- Audio is embedded as an HTML5 player using remote URLs.
- The recorder companion is available at scratch/speaking_practice_app.html.
- A new deck has been generated under decks/03_Languages/English/Speaking/01_Speaking_Practice/.
