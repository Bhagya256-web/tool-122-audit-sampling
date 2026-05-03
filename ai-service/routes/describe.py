import json
import os
import time
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from services.sanitiser import sanitise_input
from services.cache import get_cached, set_cached
from routes.health import record_response_time

describe_bp = Blueprint("describe", __name__)

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "describe_prompt.txt")

FALLBACK_RESPONSE = {
    "description": "Unable to generate description at this time. Please try again later.",
    "risk_level": "Unknown",
    "risk_justification": "AI service unavailable",
    "compliance_status": "Requires Review",
    "key_observations": [],
    "suggested_focus_areas": [],
    "is_fallback": True,
}


def load_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


@describe_bp.route("/describe", methods=["POST"])
def describe():
    start_time = time.time()

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    # Required field validation
    required = ["item_name", "department", "sample_size", "period"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    # Sanitise inputs
    for field in ["item_name", "department", "period", "notes"]:
        if data.get(field):
            cleaned, suspicious = sanitise_input(str(data[field]))
            if suspicious:
                return jsonify({"error": f"Invalid input in field: {field}"}), 400
            data[field] = cleaned

    # Check cache first
    cached = get_cached("describe", data)
    if cached:
        cached["from_cache"] = True
        return jsonify(cached), 200

    # Build prompt
    try:
        prompt = load_prompt().format(
            item_name=data.get("item_name", ""),
            department=data.get("department", ""),
            sample_size=data.get("sample_size", ""),
            period=data.get("period", ""),
            notes=data.get("notes", "None provided"),
        )
    except Exception as e:
        return jsonify({"error": f"Failed to load prompt: {str(e)}"}), 500

    # Call Groq
    try:
        messages = [{"role": "user", "content": prompt}]
        raw = call_groq(messages, temperature=0.3, max_tokens=1000)
        raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        result = json.loads(raw)
        result["is_fallback"] = False
        result["from_cache"] = False
        set_cached("describe", data, result)
    except Exception:
        result = FALLBACK_RESPONSE.copy()
        result["from_cache"] = False

    # Record response time
    duration_ms = (time.time() - start_time) * 1000
    record_response_time(duration_ms)

    result["generated_at"] = datetime.now(timezone.utc).isoformat()
    return jsonify(result), 200