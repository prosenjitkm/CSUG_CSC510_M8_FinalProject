"""
Astrology Controller
REST API endpoints for astrology decision-support analysis.
"""
from flask import Blueprint, jsonify, request

from astrology_ai import (
    SIGN_PROFILES,
    UserProfile,
    build_analysis,
    detect_sign,
    format_analysis_text,
    normalize_birthdate,
    normalize_birthtime,
    zodiac_from_birthdate,
)
from models.hash_table import HashTable
from services.disclaimers import get_disclosure_payload
from services.geocoding import geocode_with_nominatim

astrology_bp = Blueprint("astrology", __name__)

# In-memory session memory by session_id
_session_memories = {}
_geocode_cache = {}


def get_memory(session_id: str) -> HashTable:
    if session_id not in _session_memories:
        _session_memories[session_id] = HashTable(size=16)
    return _session_memories[session_id]


@astrology_bp.route("/signs", methods=["GET"])
def list_signs():
    return jsonify({"signs": sorted(SIGN_PROFILES.keys())}), 200


@astrology_bp.route("/disclosures", methods=["GET"])
def disclosures():
    return jsonify({"success": True, "disclosures": get_disclosure_payload()}), 200


@astrology_bp.route("/analyze", methods=["POST"])
def analyze():
    try:
        payload = request.json or {}
        statement = (payload.get("statement") or "").strip()
        sign = (payload.get("sign") or "").strip().lower()
        session_id = (payload.get("session_id") or "default").strip()
        full_name = (payload.get("full_name") or "").strip()
        date_of_birth = (payload.get("date_of_birth") or "").strip()
        time_of_birth = (payload.get("time_of_birth") or "").strip()
        location_of_birth = (payload.get("location_of_birth") or "").strip()

        if not statement:
            return jsonify({"success": False, "error": "No statement provided"}), 400
        if not full_name:
            return jsonify({"success": False, "error": "Full name is required"}), 400
        if not date_of_birth:
            return jsonify({"success": False, "error": "Date of birth is required"}), 400
        if not time_of_birth:
            return jsonify({"success": False, "error": "Time of birth is required"}), 400
        if not location_of_birth:
            return jsonify({"success": False, "error": "Location of birth is required"}), 400

        normalized_dob = normalize_birthdate(date_of_birth)
        if not normalized_dob:
            return jsonify(
                {
                    "success": False,
                    "error": "Invalid date_of_birth. Use YYYY-MM-DD (preferred) or MM/DD/YYYY.",
                }
            ), 400

        normalized_tob = normalize_birthtime(time_of_birth)
        if not normalized_tob:
            return jsonify(
                {
                    "success": False,
                    "error": "Invalid time_of_birth. Use HH:MM (24h) or hh:mm AM/PM.",
                }
            ), 400

        sign_source = "manual_input"
        if not sign:
            from_statement = detect_sign(statement)
            if from_statement:
                sign = from_statement
                sign_source = "statement_text"
            else:
                from_dob = zodiac_from_birthdate(normalized_dob)
                if from_dob:
                    sign = from_dob
                    sign_source = "birth_date"
                else:
                    sign = "libra"
                    sign_source = "fallback_default"

        if sign not in SIGN_PROFILES:
            return jsonify(
                {
                    "success": False,
                    "error": f"Unknown zodiac sign: {sign}",
                    "valid_signs": sorted(SIGN_PROFILES.keys()),
                }
            ), 400

        user_profile = UserProfile(
            full_name=full_name,
            date_of_birth=normalized_dob,
            time_of_birth=normalized_tob,
            location_of_birth=location_of_birth,
        )

        location_key = location_of_birth.strip().lower()
        if location_key in _geocode_cache:
            external_api_result = dict(_geocode_cache[location_key])
            external_api_result["cached"] = True
            external_api_result["details"] = (
                f"{external_api_result.get('details', 'Geocoding completed.')} Returned from in-memory cache."
            )
        else:
            external_api_result = geocode_with_nominatim(location_of_birth)
            external_api_result["cached"] = False
            _geocode_cache[location_key] = external_api_result

        memory = get_memory(session_id)
        analysis = build_analysis(
            statement=statement,
            sign=sign,
            memory=memory,
            user_profile=user_profile,
            sign_source=sign_source,
            external_api_result=external_api_result,
        )
        response_text = format_analysis_text(analysis)

        return jsonify(
            {
                "success": True,
                "sign": sign,
                "sign_source": sign_source,
                "session_id": session_id,
                "response": response_text,
                "analysis_details": {
                    "sign_source": analysis["sign_source"],
                    "tokens": analysis["tokens"],
                    "intent": analysis["intent"],
                    "confidence": analysis["confidence"],
                    "knowledge_representation": analysis["knowledge_representation"],
                    "signal_scores": analysis["signal_scores"],
                    "decision_topics": analysis["decision_topics"],
                    "matched_factors": analysis["matched_factors"],
                    "expert_rule_hits": analysis["expert_rule_hits"],
                    "symbolic_plan": analysis["symbolic_plan"],
                    "follow_up_questions": analysis["follow_up_questions"],
                    "selected_recommendations": analysis["selected_recommendations"],
                    "recommendation_pool": analysis["recommendation_pool"],
                    "pipeline_steps": analysis["pipeline_steps"],
                    "libraries_and_modules": analysis["libraries_and_modules"],
                    "disclosures": analysis["disclosures"],
                    "external_api": analysis["external_api"],
                },
            }
        ), 200

    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500
