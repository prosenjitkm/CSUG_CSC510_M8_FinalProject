# Portfolio Project Evaluation

## Project
Astrology AI Decision Support Assistant

## Requirement Coverage

### 1. Self-executable Python program
- `python astrology_ai.py` (CLI)
- `python app.py` (web UI)

### 2. Human interaction for decision support
- CLI conversational loop with profile capture and repeated Q&A.
- Web form with required user profile fields and response rendering.

### 3. Uses methods from at least 2 course modules
- Module 4 (Search): BFS and A* symbolic planning.
- Module 5 (Expert systems): condition->conclusion rule checks.
- Module 7 (Reasoning): deterministic token/phrase intent inference.
- Module 8 (Symbolic planning): state-action graph to `decision_ready`.

### 4. Reasonable answers without error
- Required field validation on UI, API, and CLI.
- Date/time normalization and fallback sign resolution.
- Controlled error responses for invalid input.

## AI/Engineering Components
- `models.set_operations.Set`: keyword overlap scoring.
- `models.sorting.QuickSelect`: top recommendation ranking.
- `models.hash_table.HashTable`: session intent memory.
- `collections.deque`, `heapq`: BFS and A* execution.
- `services.geocoding.geocode_with_nominatim`: location geocoding metadata.

## Current Required Inputs
- Full name
- Gender (`male/female` or `M/F`)
- Date of birth
- Time of birth
- Location of birth
- User question/statement

## Explainability Coverage
- Sign source and normalized profile fields
- Intent confidence and signal scores
- Decision-topic matches and follow-up prompts
- Expert rule hits
- Symbolic planning steps (BFS/A* metrics)
- External API request details
- Ethical/privacy/source disclosures

## Gap Analysis vs Common Indian Astrology Forms
The app now includes core profile fields but still omits some full-kundli controls:
- explicit timezone / DST override
- manual latitude/longitude override
- seconds-level birth time precision
- ayanamsha selection
- house-system/chart preference

These are optional future enhancements if you want stricter Vedic chart fidelity.
