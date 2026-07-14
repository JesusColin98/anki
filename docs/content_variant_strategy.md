# Content variant strategy

## Recommendation
Do not duplicate the same content across many folders in Anki. Instead, keep one canonical source of truth per scenario or skill cluster and generate deterministic variants from it.

## Proposed model
1. Canonical source
   - One JSON file per scenario or skill area.
   - Each record contains: prompt, explanation, Spanish, tags, and metadata.
2. Variant layer
   - A deterministic generator transforms the same source item into multiple exercise types:
     - speaking
     - listening
     - writing
     - dialogue
3. Deck layer
   - Each generated variant is written to its own deck or subdeck.
   - The deck is grouped by exercise type, but the content still comes from one shared source.
4. Reuse/refresh layer
   - New content should be added once in the canonical source.
   - Variants are generated from that same source, which reduces repetition and keeps the system consistent.

## Why this is better
- No duplicated maintenance work.
- Easier to keep quality high.
- Easy to expand to future variants such as roleplay, summarizing, or error-correction drills.
- Great for token efficiency because the generation logic is deterministic and template-based.

## Suggested rule of thumb
- Keep source content at the scenario level.
- Generate variants with templates rather than asking the model to invent everything from scratch each time.
- Reserve LLM usage for enrichment only, not for the full card generation loop.
