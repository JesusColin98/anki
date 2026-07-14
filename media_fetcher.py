#!/usr/bin/env python3
"""Media Fetcher — Offline Audio Downloader for Anki.

PHASE 2 ONLY: This script is designed now but not executed in Phase 1.
Phase 1 uses URL links embedded in card 'audio_links' fields.

When activated, this script:
  1. Reads all JSON deck files under decks/.
  2. Finds cards with 'audio_links' fields.
  3. Downloads the audio (MP3/OGG) from each URL.
  4. Stores each file in Anki's media collection via AnkiConnect.storeMediaFile.

Architecture:
  - Data stays in JSON (URLs only).
  - Binary audio files live only in Anki's local media folder.
  - No audio files in the git repository (lightweight repo).

Usage (Phase 2):
  python media_fetcher.py --dry-run          # List what would be downloaded
  python media_fetcher.py --pattern flap_t   # Download for one pattern only
  python media_fetcher.py                    # Download all missing audio
"""

import argparse
import base64
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = Path(__file__).parent.resolve()
DECKS_DIR = BASE_DIR / "decks"
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

# Rate limiting — be respectful to public servers
REQUEST_DELAY_SECONDS = 1.5
MAX_CONSECUTIVE_FAILURES = 3


# ---------------------------------------------------------------------------
# AnkiConnect helper
# ---------------------------------------------------------------------------

def anki_invoke(action: str, **params) -> Any:
    """Sends a request to AnkiConnect and returns the result."""
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        ANKI_CONNECT_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            if res.get("error"):
                raise RuntimeError(res["error"])
            return res["result"]
    except urllib.error.URLError:
        print("[-] Error: AnkiConnect not reachable. Is Anki Desktop running?", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Audio download
# ---------------------------------------------------------------------------

def fetch_audio_bytes(url: str) -> Optional[bytes]:
    """Downloads audio bytes from a public URL with retry logic.

    Implements exponential backoff on failures (max 3 consecutive errors).

    Args:
        url: Public audio URL.

    Returns:
        Raw bytes of the audio file, or None on failure.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; AnkiMediaFetcher/1.0; "
            "+https://github.com/anki-tools)"
        )
    }
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(MAX_CONSECUTIVE_FAILURES):
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                # Rate limited — exponential backoff
                wait = REQUEST_DELAY_SECONDS * (2 ** attempt)
                print(f"    [!] Rate limited (429). Waiting {wait:.1f}s...")
                time.sleep(wait)
            else:
                print(f"    [!] HTTP {e.code} for {url}")
                return None
        except Exception as e:
            print(f"    [!] Error fetching {url}: {e}")
            return None
    print(f"    [-] Aborting after {MAX_CONSECUTIVE_FAILURES} failures for {url}")
    return None


def store_media_in_anki(filename: str, audio_bytes: bytes) -> bool:
    """Stores a media file in Anki's collection via AnkiConnect.storeMediaFile.

    Args:
        filename: Target filename in Anki media folder (e.g. 'flap_t_water.mp3').
        audio_bytes: Raw audio bytes.

    Returns:
        True if stored successfully.
    """
    b64_data = base64.b64encode(audio_bytes).decode("utf-8")
    try:
        anki_invoke("storeMediaFile", filename=filename, data=b64_data)
        return True
    except Exception as e:
        print(f"    [-] Failed to store '{filename}' in Anki: {e}")
        return False


# ---------------------------------------------------------------------------
# Deck scanner
# ---------------------------------------------------------------------------

def find_deck_files(pattern_filter: Optional[str] = None) -> List[Path]:
    """Finds all JSON deck files, optionally filtered by filename pattern.

    Args:
        pattern_filter: Optional substring to match in the file stem (e.g. 'flap_t').

    Returns:
        List of Path objects for matching JSON files.
    """
    all_files = list(DECKS_DIR.rglob("*.json"))
    if pattern_filter:
        all_files = [f for f in all_files if pattern_filter.lower() in f.stem.lower()]
    return all_files


def extract_audio_links(deck_file: Path) -> List[Tuple[str, str, str]]:
    """Extracts (card_id, label, url) tuples from a deck JSON file.

    Args:
        deck_file: Path to a deck JSON file.

    Returns:
        List of (card_identifier, link_label, url) tuples.
    """
    with open(deck_file, "r", encoding="utf-8") as f:
        cards = json.load(f)

    results = []
    for i, card in enumerate(cards):
        audio_links = card.get("audio_links", {})
        if not audio_links:
            continue
        # Build a stable filename prefix from deck path + card index
        deck_slug = card.get("deck", "unknown").replace("::", "_").replace(" ", "_")
        for label, url in audio_links.items():
            if url and url.startswith("http"):
                # Skip non-downloadable page URLs (Forvo pages, YouGlish, etc.)
                # Only download direct MP3/OGG audio file URLs
                if any(url.endswith(ext) for ext in (".mp3", ".ogg", ".wav", ".m4a")):
                    filename = f"{deck_slug}__{label}_{i:04d}.mp3"
                    results.append((deck_slug, filename, url))
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(dry_run: bool = False, pattern_filter: Optional[str] = None) -> None:
    """Main entry point for the media fetcher.

    Args:
        dry_run: If True, only lists what would be downloaded without fetching.
        pattern_filter: Optional pattern to filter deck files by name.
    """
    deck_files = find_deck_files(pattern_filter)
    print(f"[+] Scanning {len(deck_files)} deck file(s)...")

    all_audio: List[Tuple[str, str, str]] = []
    for deck_file in deck_files:
        links = extract_audio_links(deck_file)
        if links:
            print(f"    Found {len(links)} audio link(s) in {deck_file.name}")
            all_audio.extend(links)

    if not all_audio:
        print("[*] No downloadable audio URLs found (Phase 1 uses browser-link URLs).")
        print("    Add direct MP3 URLs to card 'audio_links' fields to enable download.")
        return

    print(f"\n[+] Total audio files to process: {len(all_audio)}")

    if dry_run:
        print("\n=== DRY RUN — Files that would be downloaded ===")
        for _, filename, url in all_audio:
            print(f"  {filename}  <-  {url}")
        return

    # Download and store
    consecutive_failures = 0
    stored = 0

    for deck_slug, filename, url in all_audio:
        print(f"  Downloading: {filename}")
        audio_bytes = fetch_audio_bytes(url)

        if audio_bytes is None:
            consecutive_failures += 1
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                print(f"[-] Aborting: {MAX_CONSECUTIVE_FAILURES} consecutive failures reached.")
                sys.exit(1)
            continue

        consecutive_failures = 0
        if store_media_in_anki(filename, audio_bytes):
            print(f"    [✓] Stored: {filename}")
            stored += 1
        time.sleep(REQUEST_DELAY_SECONDS)

    print(f"\n[✓] Done. {stored}/{len(all_audio)} audio files stored in Anki media.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Anki Media Fetcher — Download audio into Anki's media collection."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List what would be downloaded without fetching anything.",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default=None,
        help="Filter deck files by filename pattern (e.g. 'flap_t').",
    )
    args = parser.parse_args()
    main(dry_run=args.dry_run, pattern_filter=args.pattern)
