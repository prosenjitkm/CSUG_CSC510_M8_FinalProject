"""
Geocoding service for astrology app.
Uses OpenStreetMap Nominatim search API.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict
from urllib.parse import urlencode
from urllib.request import Request, urlopen


NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "csc506-astrology-ai/1.0 (educational project)"


def geocode_with_nominatim(location: str, timeout: int = 8) -> Dict[str, Any]:
    location = (location or "").strip()
    if not location:
        return {
            "used": False,
            "success": False,
            "provider": "OpenStreetMap Nominatim",
            "query": location,
            "details": "No location provided.",
        }

    params = {
        "q": location,
        "format": "jsonv2",
        "limit": 1,
        "addressdetails": 1,
    }
    request_url = f"{NOMINATIM_BASE_URL}?{urlencode(params)}"
    request = Request(
        request_url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )

    start = time.time()
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            status = response.status
    except Exception as exc:
        return {
            "used": True,
            "success": False,
            "provider": "OpenStreetMap Nominatim",
            "query": location,
            "request_url": request_url,
            "http_status": None,
            "duration_ms": round((time.time() - start) * 1000, 2),
            "details": f"Geocoding request failed: {exc}",
        }

    duration_ms = round((time.time() - start) * 1000, 2)
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {
            "used": True,
            "success": False,
            "provider": "OpenStreetMap Nominatim",
            "query": location,
            "request_url": request_url,
            "http_status": status,
            "duration_ms": duration_ms,
            "details": "Received non-JSON response from geocoding API.",
        }

    if not payload:
        return {
            "used": True,
            "success": False,
            "provider": "OpenStreetMap Nominatim",
            "query": location,
            "request_url": request_url,
            "http_status": status,
            "duration_ms": duration_ms,
            "details": "No matching location found.",
        }

    best = payload[0]
    lat = float(best.get("lat"))
    lon = float(best.get("lon"))

    return {
        "used": True,
        "success": True,
        "provider": "OpenStreetMap Nominatim",
        "query": location,
        "request_url": request_url,
        "http_status": status,
        "duration_ms": duration_ms,
        "coordinates": {
            "latitude": lat,
            "longitude": lon,
        },
        "top_result": {
            "display_name": best.get("display_name"),
            "type": best.get("type"),
            "importance": best.get("importance"),
            "osm_type": best.get("osm_type"),
            "osm_id": best.get("osm_id"),
        },
        "details": "Location successfully geocoded via external API.",
    }
