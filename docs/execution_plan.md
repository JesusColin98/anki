# Execution plan for the Anki content system

## Phase 1 — Stabilize the content model
1. Keep the existing deck JSON files as the source of truth for scenario-based cards.
2. Add a small metadata layer for each card:
   - scenario_id
   - skill_area
   - difficulty
   - variant_type
   - source_hash
3. Make sure every generated card can trace back to a canonical source item.

## Phase 2 — Create deterministic variant generators
1. Implement a base generator for:
   - speaking
   - listening
   - writing
   - dialogue
2. Each variant is generated from the same source card using simple templates.
3. Keep the logic deterministic to avoid token waste and repetition.

## Phase 3 — Add a lightweight speaking workflow
1. Keep remote audio by default.
2. Add a recorder companion link for self-practice.
3. Use a dedicated speaking model in Anki for prompt + audio + recorder integration.

## Phase 4 — Create a refresh and reuse loop
1. When a canonical scenario is updated, regenerate its variants.
2. Preserve the same source IDs so the system can track drift.
3. Avoid adding new cards manually when a variant can be generated automatically.

## Phase 5 — Expand into richer exercise formats
1. Add multi-turn dialogues.
2. Add comprehension / summary cards.
3. Add error-correction drills.
4. Add spaced review prompts tied to the same source concept.

## Phase 6 — Optimize for Anki usability
1. Keep front sides short and readable.
2. Keep backs structured with explanation + example + translation.
3. Use a small number of reusable templates instead of many bespoke ones.
4. Keep audio optional and remote-first to reduce bloat.
