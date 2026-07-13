#!/usr/bin/env python3
"""Article & News Scraper Agent for Anki Flashcard Generation.

Fetches web articles, extracts core technical facts, cleans noise, and formats
them into atomic Anki Cloze & Scenario flashcards saved into the decks/ tree.
"""

import json
from pathlib import Path
import re
import sys
import urllib.parse
from bs4 import BeautifulSoup
import requests

BASE_DIR = Path(__file__).parent.resolve()
DECKS_DIR = BASE_DIR / "decks"


def scrape_article(url: str) -> dict:
  """Fetch and extract clean readable content from a news or article URL."""
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/115.0.0.0 Safari/537.36"
      )
  }
  print(f"[+] Scraping article from: {url}")
  resp = requests.get(url, headers=headers, timeout=15)
  resp.raise_for_status()

  soup = BeautifulSoup(resp.text, "html.parser")

  # Remove unwanted tags
  for tag in soup(
      ["script", "style", "nav", "footer", "header", "aside", "form"]
  ):
    tag.decompose()

  title = (
      soup.title.string.strip() if soup.title else "Untitled Scraped Article"
  )
  h1 = soup.find("h1")
  if h1:
    title = h1.get_text(strip=True)

  paragraphs = []
  for p in soup.find_all("p"):
    txt = p.get_text(strip=True)
    if len(txt) > 40:  # Ignore short fragments
      paragraphs.append(txt)

  code_blocks = [code.get_text() for code in soup.find_all("code")]

  return {
      "title": title,
      "url": url,
      "paragraphs": paragraphs,
      "code_blocks": code_blocks,
      "full_text": "\n\n".join(paragraphs),
  }


def generate_flashcards_from_article(
    article_data: dict, deck_name: str = "News_Scraped::General"
) -> list:
  """Extract atomic facts and format them into Cloze deletion cards."""
  title = article_data["title"]
  paragraphs = article_data["paragraphs"]
  cards = []

  # Clean deck category name for tagging
  category_tag = re.sub(r"\W+", "_", deck_name.split("::")[-1]).lower()

  for i, p in enumerate(paragraphs[:10]):  # Process top 10 key paragraphs
    # Simple rule-based cloze extraction for key sentences
    sentences = re.split(r"(?<=[.!?]) +", p)
    for s in sentences:
      if len(s) < 30 or len(s) > 200:
        continue

      # Highlight potential keywords (Capitalized terms or technical words)
      words = s.split()
      if len(words) > 6:
        # Pick a key middle word or entity for Cloze deletion
        target_idx = max(2, len(words) // 2)
        target_word = words[target_idx].strip(".,;:\"'")
        if len(target_word) > 3:
          cloze_text = s.replace(target_word, f"{{{{c1::{target_word}}}}}")

          card = {
              "deck": deck_name,
              "scenario": f"News & Articles 📰 ({title[:30]})",
              "text": cloze_text,
              "explanation": (
                  f"Extract from article: <strong>{title}</strong>.<br>Source:"
                  f' <a href="{article_data["url"]}">{article_data["url"]}</a>'
              ),
              "usage": (
                  f"Context: <code>{s}</code><ul><li>Source: {title}</li></ul>"
              ),
              "spanish": f"Extraído de: {title}",
              "tags": ["news_scraped", category_tag],
          }
          cards.append(card)
          if len(cards) >= 5:  # Limit per article
            break
    if len(cards) >= 5:
      break

  return cards


def save_cards_to_deck(cards: list, deck_name: str):
  """Save generated cards into the appropriate subfolder under decks/."""
  rel_path = deck_name.replace("::", "/") + ".json"
  target_file = DECKS_DIR / rel_path
  target_file.parent.mkdir(parents=True, exist_ok=True)

  existing_cards = []
  if target_file.exists():
    with open(target_file, "r", encoding="utf-8") as f:
      try:
        existing_cards = json.load(f)
      except Exception:
        existing_cards = []

  # De-duplicate by text
  seen_texts = {c["text"] for c in existing_cards}
  new_added = 0
  for c in cards:
    if c["text"] not in seen_texts:
      existing_cards.append(c)
      seen_texts.add(c["text"])
      new_added += 1

  with open(target_file, "w", encoding="utf-8") as f:
    json.dump(existing_cards, f, indent=2, ensure_ascii=False)

  print(f"[+] Added {new_added} new cards to: decks/{rel_path}")


def main():
  if len(sys.argv) < 2:
    print("Usage: python3 scraper_agent.py <URL> [deck_name]")
    print(
        "Example: python3 scraper_agent.py https://example.com/article"
        " News_Scraped::AI_Trends"
    )
    sys.exit(1)

  url = sys.argv[1]
  deck_name = sys.argv[2] if len(sys.argv) > 2 else "News_Scraped::General"

  article = scrape_article(url)
  print(
      f"[+] Extracted '{article['title']}' ({len(article['paragraphs'])}"
      " paragraphs)"
  )

  cards = generate_flashcards_from_article(article, deck_name)
  print(f"[+] Formatted {len(cards)} Anki cards.")

  save_cards_to_deck(cards, deck_name)


if __name__ == "__main__":
  main()
