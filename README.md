# Astrology AI — Decision Support Assistant
### CSC510 Module 8 Final Project

An astrology-themed decision-support application built with Python and Flask. It accepts a user's birth profile and a natural-language question, then returns structured, rule-based guidance using classical zodiac profiles, intent detection, expert rules, and symbolic planning.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Setup & Installation](#setup--installation)
5. [Running the Application](#running-the-application)
6. [Using the CLI Mode](#using-the-cli-mode)
7. [Using the Web Interface](#using-the-web-interface)
8. [API Reference](#api-reference)
9. [Data Structures & Algorithms](#data-structures--algorithms)
10. [Services](#services)
11. [Disclaimers](#disclaimers)

---

## Overview

Astrology AI takes a user's birth profile (name, gender, date of birth, time of birth, birth location) and a free-text decision question, then produces a structured guidance report including:

- Zodiac sign detection (from input text, birth date, or manual entry)
- Intent classification (career, love, money, health, family, general)
- Confidence-weighted signal scoring
- Expert-rule evaluation
- Symbolic decision planning via graph traversal (BFS)
- Top-K recommendation selection via QuickSelect
- Birth-location geocoding via OpenStreetMap Nominatim
- Ethical disclaimers and privacy notices

The project runs in two modes:
- **Web App** — Flask REST API + HTML/JS front end
- **CLI** — standalone terminal program (`astrology_ai.py`)

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
│  Browser (astrology.html + astrology.js + astrology.css)         │
│  or CLI (python astrology_ai.py)                                 │
└───────────────────┬──────────────────────────────────────────────┘
                    │ HTTP / direct call
┌───────────────────▼──────────────────────────────────────────────┐
│                     Flask Application (app.py)                   │
│  CORS-enabled Flask app                                          │
│  Routes: / and /astrology → renders astrology.html               │
│  Blueprint: /api/astrology → astrology_controller.py             │
└───────────────────┬──────────────────────────────────────────────┘
                    │
┌───────────────────▼──────────────────────────────────────────────┐
│              Controller (controllers/astrology_controller.py)    │
│  - Input validation & normalization                              │
│  - Session memory management (HashTable per session_id)          │
│  - In-memory geocode cache                                       │
│  - Delegates to astrology_ai.build_analysis()                    │
└──────┬────────────────────────────────┬───────────────────────────┘
       │                                │
┌──────▼──────────────────┐   ┌─────────▼──────────────────────────┐
│  Core AI Engine          │   │  Services                          │
│  (astrology_ai.py)       │   │  ├── geocoding.py (Nominatim API)  │
│                          │   │  ├── decision_topics.py            │
│  - Sign profiles         │   │  │   (topic detection & scoring)   │
│  - Intent detection      │   │  └── disclaimers.py               │
│  - Confidence scoring    │   │      (ethical disclosure text)     │
│  - Expert rule engine    │   └────────────────────────────────────┘
│  - Symbolic BFS planner  │
│  - Recommendation engine │
│  - format_analysis_text()|
└──────┬───────────────────┘
       │
┌──────▼──────────────────────────────────────────────────────────┐
│                     Models (Data Structures)                     │
│  ├── hash_table.py   — chained HashTable (session memory)        │
│  ├── set_operations.py — custom Set (union, intersection, etc.)  │
│  └── sorting.py       — QuickSelect (top-K recommendations)      │
└─────────────────────────────────────────────────────────────────┘
```

### Request Flow (Web Mode)

1. User fills out the form in the browser and clicks **Analyze**.
2. `astrology.js` sends a `POST /api/astrology/analyze` request with the user's profile and question.
3. `astrology_controller.py` validates and normalizes all inputs, looks up or creates a session `HashTable`, and calls `geocode_with_nominatim()`.
4. `astrology_ai.build_analysis()` runs the full pipeline: tokenization → intent detection → confidence scoring → expert rules → BFS symbolic plan → QuickSelect top-3 recommendations.
5. The JSON response is returned and rendered in the browser.

---

## Project Structure

```
CSUG_CSC510_M8_FinalProject/
│
├── app.py                          # Flask entry point, blueprint registration
├── astrology_ai.py                 # Core AI engine + CLI runner
│
├── controllers/
│   ├── __init__.py
│   └── astrology_controller.py     # REST API endpoints (Flask Blueprint)
│
├── models/
│   ├── __init__.py
│   ├── hash_table.py               # Custom HashTable with chaining
│   ├── set_operations.py           # Custom Set with union/intersection/difference
│   └── sorting.py                  # QuickSelect algorithm
│
├── services/
│   ├── __init__.py
│   ├── decision_topics.py          # Topic detection, intent boosting, follow-up Qs
│   ├── disclaimers.py              # Ethical & transparency disclosure strings
│   └── geocoding.py                # OpenStreetMap Nominatim geocoding
│
├── static/
│   ├── css/
│   │   └── astrology.css           # Front-end styles
│   └── js/
│       └── astrology.js            # Front-end logic (fetch API calls)
│
└── templates/
    └── astrology.html              # Jinja2 template for the web UI
```

---

## Setup & Installation

### Prerequisites

- Python 3.9 or higher
- pip

### 1. Clone / open the project

```bash
cd C:\Users\prose\PycharmProjects\CSUG_CSC510_M8_FinalProject
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate        # Windows PowerShell
# source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install flask flask-cors
```

> The geocoding service uses only Python's built-in `urllib` — no extra HTTP library is required.

---

## Running the Application

### Web App (Flask)

```bash
python app.py
```

The server starts at **http://localhost:5000**.
Open your browser and navigate to `http://localhost:5000` or `http://localhost:5000/astrology`.

Logs are printed to the console in the format:
```
YYYY-MM-DD HH:MM:SS - name - LEVEL - message
```

To stop the server press `Ctrl+C`.

---

## Using the CLI Mode

Run the standalone CLI program directly — no Flask server is needed:

```bash
python astrology_ai.py
```

You will be prompted to enter:

| Prompt | Example input |
|--------|---------------|
| Full name | `Jane Doe` |
| Gender (M/F) | `F` |
| Date of birth | `1990-06-15` or `06/15/1990` |
| Time of birth | `14:30` or `2:30 PM` |
| Location of birth | `New York, USA` |
| Your question | `Should I switch my job this year?` |

Type `exit` or `quit` to close. Type `help` or `examples` for sample questions. Type `disclaimer` or `privacy` to read the full disclosure.

---

## Using the Web Interface

1. Start the Flask server (`python app.py`).
2. Open `http://localhost:5000` in your browser.
3. Fill in all profile fields and your decision question.
4. Click **Analyze**. The guidance report will appear on the page.

The front end calls these API endpoints automatically:
- `GET /api/astrology/disclosures` — loads disclaimer text on page load
- `GET /api/astrology/signs` — loads the list of valid zodiac signs
- `POST /api/astrology/analyze` — submits the profile and question

---

## API Reference

Base URL: `http://localhost:5000/api/astrology`

### `GET /signs`

Returns the list of all supported zodiac signs.

**Response**
```json
{
  "signs": ["aquarius", "aries", "cancer", ...]
}
```

---

### `GET /disclosures`

Returns ethical disclaimers and privacy notices.

**Response**
```json
{
  "success": true,
  "disclosures": {
    "main_disclaimer": "...",
    "short_disclaimer": "...",
    "data_privacy_notice": "...",
    "sources_note": "..."
  }
}
```

---

### `POST /analyze`

Runs the full decision-support analysis.

**Request Body (JSON)**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `statement` | string | ✅ | The user's question or decision statement |
| `full_name` | string | ✅ | User's full name |
| `gender` | string | ✅ | `male`, `female`, `M`, or `F` |
| `date_of_birth` | string | ✅ | `YYYY-MM-DD` or `MM/DD/YYYY` |
| `time_of_birth` | string | ✅ | `HH:MM` (24h) or `hh:mm AM/PM` |
| `location_of_birth` | string | ✅ | Free-text location, e.g. `London, UK` |
| `sign` | string | ❌ | Override zodiac sign (auto-detected if omitted) |
| `session_id` | string | ❌ | Session identifier for memory; defaults to `"default"` |

**Example Request**
```json
{
  "statement": "Should I get married this year?",
  "full_name": "Jane Doe",
  "gender": "F",
  "date_of_birth": "1990-06-15",
  "time_of_birth": "14:30",
  "location_of_birth": "London, UK",
  "session_id": "user-42"
}
```

**Example Response**
```json
{
  "success": true,
  "sign": "gemini",
  "sign_source": "birth_date",
  "gender": "female",
  "session_id": "user-42",
  "response": "Astrology AI — Decision Support\n...",
  "analysis_details": {
    "intent": "love",
    "confidence": 82,
    "signal_scores": { "love": 82, "general": 10 },
    "decision_topics": [...],
    "expert_rule_hits": [...],
    "symbolic_plan": {...},
    "follow_up_questions": [...],
    "selected_recommendations": [...],
    "disclosures": {...},
    "external_api": {...}
  }
}
```

**Error Response**
```json
{
  "success": false,
  "error": "Date of birth is required"
}
```

---

## Data Structures & Algorithms

### HashTable (`models/hash_table.py`)

A custom hash table using **chaining** (each bucket is a list of `(key, value)` tuples) for collision resolution.

- Used by the controller to store per-session conversation memory.
- A separate `HashTable` instance is created per `session_id`.
- Tracks collision count and operation count for observability.
- Time complexity: O(1) average for insert/get/delete; O(n) worst case on collision chains.

### Set (`models/set_operations.py`)

A custom `Set` class wrapping Python's built-in `set`, with explicit methods for:

| Operation | Description |
|-----------|-------------|
| `union` | A ∪ B — elements in A or B or both |
| `intersection` | A ∩ B — elements in both A and B |
| `difference` | A − B — elements in A not in B |
| `symmetric_difference` | (A ∪ B) − (A ∩ B) |
| `add` / `remove` / `contains` | Standard membership operations |

Used in the AI engine to compute matched intent factors from token sets.

### QuickSelect (`models/sorting.py`)

An in-place **QuickSelect** algorithm (partition-based, O(n) average) used to find the top-K recommendations from a scored recommendation pool.

- Selects the top 3 recommendations by score without fully sorting the pool.
- Tracks comparisons, partitions, and execution time for observability.

### Graph / BFS Symbolic Planner (`astrology_ai.py`)

A directed graph is built per intent (e.g., `career`, `love`) with labeled edges (actions). **Breadth-First Search** finds the shortest action path from `"start"` to `"decision_ready"`, forming the *suggested decision path* shown in the response.

### Priority Queue (`astrology_ai.py`)

Python's `heapq` module is used to rank and select expert rules and signal scores by priority weight.

---

## Services

### `services/geocoding.py`

Calls the **OpenStreetMap Nominatim** API to resolve a free-text birth location into latitude/longitude coordinates. Results are cached in memory per session to avoid redundant external calls.

- No API key required.
- Falls back gracefully with a `success: false` payload if the request fails or times out.

### `services/decision_topics.py`

Provides three functions used by the AI engine:

- `detect_decision_topics(tokens)` — scans tokenized input against a keyword dictionary and returns matched topic objects (label, intent, factors).
- `boost_intent_scores(scores, topics)` — adds weighted boosts to intent scores when topic keywords are found.
- `follow_up_questions(intent)` — returns 3 clarifying questions relevant to the detected intent category.

### `services/disclaimers.py`

Provides a `get_disclosure_payload()` function that returns a dictionary of four disclosure strings:

- `main_disclaimer` — general informational-only notice
- `short_disclaimer` — brief reminder shown in responses
- `data_privacy_notice` — explains no persistent storage is used
- `sources_note` — describes the deterministic methods used

---

## Disclaimers

This application is built for **educational purposes** as a CSC510 coursework project. It does **not** provide medical, legal, financial, or mental-health advice. All guidance is generated by deterministic rule tables and symbolic planning — not by a trained AI model or licensed professional. Location data is processed in-memory only; no data is persisted to a database.

