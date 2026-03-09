"""
Ethical and transparency disclaimers for the Astrology AI app.
"""

from __future__ import annotations

from typing import Dict


MAIN_DISCLAIMER = (
    "This system provides informational and cultural astrology guidance only. "
    "It is not a substitute for medical, legal, financial, or mental-health advice."
)

SHORT_DISCLAIMER = (
    "Use this output as one input in your decision-making, not as certainty."
)

DATA_PRIVACY_NOTICE = (
    "Profile fields are used only to compute in-session guidance. "
    "No persistent database storage is used by this app."
)

SOURCES_NOTE = (
    "Methods are based on deterministic rule tables (zodiac profiles, keyword intent mapping, "
    "expert-rule checks, and symbolic planning search). Location coordinates are fetched from "
    "OpenStreetMap Nominatim when geocoding is enabled."
)


def get_disclosure_payload() -> Dict[str, str]:
    return {
        "main_disclaimer": MAIN_DISCLAIMER,
        "short_disclaimer": SHORT_DISCLAIMER,
        "data_privacy_notice": DATA_PRIVACY_NOTICE,
        "sources_note": SOURCES_NOTE,
    }
