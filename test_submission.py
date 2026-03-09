"""
Pre-submission validation script.
Run: python test_submission.py
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


def ok(msg: str) -> None:
    print(f"[PASS] {msg}")


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def check_files() -> bool:
    required = [
        "astrology_ai.py",
        "app.py",
        "requirements.txt",
        "README_ASTROLOGY.md",
        "controllers/astrology_controller.py",
        "templates/astrology.html",
        "static/js/astrology.js",
        "services/decision_topics.py",
        "services/disclaimers.py",
        "models/hash_table.py",
        "models/set_operations.py",
        "models/sorting.py",
    ]
    all_good = True
    for path in required:
        if Path(path).exists():
            ok(f"file exists: {path}")
        else:
            fail(f"missing file: {path}")
            all_good = False
    return all_good


def check_imports() -> bool:
    modules = [
        "flask",
        "flask_cors",
        "astrology_ai",
        "controllers.astrology_controller",
        "services.geocoding",
    ]
    all_good = True
    for mod in modules:
        try:
            importlib.import_module(mod)
            ok(f"import: {mod}")
        except Exception as exc:
            fail(f"import failed: {mod} ({exc})")
            all_good = False
    return all_good


def check_core_logic() -> bool:
    from astrology_ai import (
        UserProfile,
        build_analysis,
        normalize_gender,
    )
    from models.hash_table import HashTable

    all_good = True
    if normalize_gender("M") == "male" and normalize_gender("female") == "female":
        ok("gender normalization")
    else:
        fail("gender normalization")
        all_good = False

    profile = UserProfile(
        full_name="Test User",
        gender="male",
        date_of_birth="1990-01-28",
        time_of_birth="12:00",
        location_of_birth="Dhaka, Bangladesh",
    )
    analysis = build_analysis(
        statement="Should I get married this year?",
        sign="aquarius",
        memory=HashTable(size=16),
        user_profile=profile,
    )
    if analysis.get("gender") == "male":
        ok("analysis carries gender")
    else:
        fail("analysis missing gender")
        all_good = False

    if analysis.get("selected_recommendations"):
        ok("recommendations generated")
    else:
        fail("recommendations missing")
        all_good = False

    return all_good


def check_api() -> bool:
    from app import app

    client = app.test_client()
    payload = {
        "full_name": "Test User",
        "gender": "F",
        "date_of_birth": "1990-01-28",
        "time_of_birth": "12:00",
        "location_of_birth": "Dhaka, Bangladesh",
        "statement": "Should I have a baby this year?",
        "session_id": "test",
    }

    all_good = True
    resp = client.post("/api/astrology/analyze", json=payload)
    if resp.status_code == 200 and resp.is_json and resp.json.get("success"):
        ok("API analyze success case")
    else:
        fail(f"API analyze success case failed ({resp.status_code})")
        all_good = False

    bad = dict(payload)
    bad["gender"] = "X"
    resp_bad = client.post("/api/astrology/analyze", json=bad)
    if resp_bad.status_code == 400:
        ok("API invalid gender rejected")
    else:
        fail(f"API invalid gender not rejected ({resp_bad.status_code})")
        all_good = False

    return all_good


def main() -> int:
    print("Running project validation checks...\n")
    checks = {
        "files": check_files(),
        "imports": check_imports(),
        "core_logic": check_core_logic(),
        "api": check_api(),
    }
    print("\nSummary:")
    all_good = True
    for name, passed in checks.items():
        print(f"- {name}: {'PASS' if passed else 'FAIL'}")
        all_good = all_good and passed
    return 0 if all_good else 1


if __name__ == "__main__":
    raise SystemExit(main())
