# Astrology AI Project (Course Submission)

## What this program does
`astrology_ai.py` is a self-executable Python CLI assistant that:
- accepts a user statement in natural language,
- requires profile details including gender, birth date, birth time, and birth location,
- identifies likely decision focus (`career`, `love`, `money`, `health`, `family`, `general`),
- detects decision topics/phrases (for example: `baby`, `marriage`, `job`, `finance`) and uses them to reduce ambiguity,
- uses astrology-style logic (zodiac profile + element + modality),
- returns structured decision-support guidance plus follow-up questions and disclosure notices.

## Course-method usage (at least 2 modules)
This app uses course-style techniques from your project code:
- `Set` operations for keyword overlap and intent detection (`models/set_operations.py`)
- `QuickSelect` algorithm for ranking/selecting top guidance (`models/sorting.py`)
- `HashTable` for session memory of repeated themes (`models/hash_table.py`)
- Uninformed search (`BFS`) and informed search (`A*`) for symbolic decision planning (`astrology_ai.py`)
- Expert-system style topic mapping for phrase-to-intent guidance (`services/decision_topics.py`)

## Requirement Mapping (Portfolio Rubric)
- Fully-functioning AI decision-support program: yes (CLI + Flask UI).
- Interacts with human users: yes (prompt/form input and contextual output).
- Self-executable Python program: yes (`python astrology_ai.py` and `python app.py`).
- Uses methods from at least 2 modules: yes (set logic, ranking, hash memory, search, symbolic planning).
- Reasonable answers without error: validated with input checks and fallback logic.

### Syllabus Concept Mapping
- Intelligent Search Methods (Module 4):
  - Uninformed search: BFS over symbolic decision-state graph.
  - Informed search: A* with heuristic distance estimates.
- Cognitive Systems / Expert Systems (Module 5):
  - Rule base (`EXPERT_RULES`) with condition->conclusion inference.
- Reasoning Systems and Logic (Module 7):
  - Deterministic intent inference using token overlap, phrase boosts, and rule triggering.
- Symbolic Planning (Module 8):
  - State-action symbolic graph for intent-specific decision plans.
- Deep Learning inclusion:
  - Not used in current version (rule-based + symbolic methods were selected for transparency and explainability).

## How to run
1. Open terminal in the project folder.
2. CLI mode:

```powershell
python astrology_ai.py
```

3. Type prompts like:
- `I'm a Virgo and I am unsure if I should switch jobs this month.`
- `As a Leo, should I text my ex or move on?`
- `I feel stressed and low energy lately, what should I focus on?`

4. Type `exit` to quit.

## Project Structure (Cleaned)
- `app.py` -> Flask UI entry point
- `astrology_ai.py` -> CLI entry point + core reasoning engine
- `controllers/astrology_controller.py` -> API layer for UI
- `services/geocoding.py` -> external geocoding API integration
- `services/decision_topics.py` -> migrated topic detection + intent boost + follow-up question generation
- `services/disclaimers.py` -> migrated disclaimer/privacy/source messaging
- `models/hash_table.py` -> session memory data structure
- `models/set_operations.py` -> set-based intent matching
- `models/sorting.py` -> QuickSelect ranking utility
- `templates/astrology.html` -> single web interface
- `static/css/astrology.css` -> UI styling
- `static/js/astrology.js` -> browser logic

## Browser UI mode
1. Start Flask app:

```powershell
python app.py
```

2. Open:
- `http://localhost:5000/` (Astrology UI)
- `http://localhost:5000/astrology` (same page alias)

3. Submit a statement in the form.  
The page calls `POST /api/astrology/analyze` and displays the generated guidance.
Additional utility endpoint:
- `GET /api/astrology/disclosures` -> returns disclaimer/privacy/source notes used by the app
Required fields in UI/API:
- full name
- gender (`male`/`female`; CLI also accepts `M`/`F`)
- date of birth (`YYYY-MM-DD` in web UI; API also accepts `MM/DD/YYYY`)
- time of birth (`HH:MM` 24-hour in web UI; API also accepts `hh:mm AM/PM`)
- location of birth
- statement/question

Validation behavior:
- the app blocks submission on missing/invalid required fields
- backend re-validates formats and returns clear errors if input is invalid
- backend enforces gender normalization (`male` or `female`)
- web page shows a normalized input preview before analysis
- web result includes a transparent reasoning trace:
  - sign source (manual, statement text, or birth date)
  - matched decision topics and their mapped intent
  - keyword signal scores
  - suggested follow-up questions
  - ranking scores for selected recommendations
  - exact modules/libraries used
  - ethical disclaimer/privacy/source notes
  - explicit external API usage status and request metadata

## External API used
- Geocoding provider: OpenStreetMap Nominatim (`https://nominatim.openstreetmap.org/search`)
- Purpose: converts birth location text into latitude/longitude
- The reasoning section shows:
  - request URL
  - HTTP status
  - response time
  - coordinates
  - top geocode result metadata (display name/type/importance)
  - whether result came from cache

Note: internet access is required for live geocoding. If the request fails, the app still returns guidance and shows the geocoding failure details.

## Notes
- The project supports two intended entry points only:
  - CLI: `python astrology_ai.py`
  - UI: `python app.py` then open `http://localhost:5000/`
- CLI profile prompts now include required `Gender (M/F)` input.
- If no zodiac sign is provided, sign is inferred from statement text or date of birth.

### Common Indian-Astrology Inputs Not Yet Implemented
For higher-fidelity Vedic-style calculations, many astrology systems also ask for:
- explicit time zone and DST correction at birth
- birth-place hierarchy (city + district/state + country) and manual latitude/longitude override
- birth time with seconds precision
- ayanamsha choice (for sidereal calculations)
- house-system / chart-style preference
- partner profile inputs for compatibility workflows

Current app version focuses on a decision-support assistant and uses a simplified transparent rule pipeline, not full kundli chart mathematics.
- Essay support files:
  - `ESSAY_OUTLINE.md` (2-4 page structure for required write-up)
  - `REFERENCES_APA.md` (APA-formatted reference suggestions)

## Migration note
This project now includes selected migration items from `C:\Users\prose\PycharmProjects\CSC510_M8`:
- topic-detection patterns adapted for decision-support prompts
- disclaimer/privacy/source transparency patterns
- expanded explainability output (topics, follow-up questions, and API details)
