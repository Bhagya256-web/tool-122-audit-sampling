import json
import os
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from services.sanitiser import sanitise_input

recommend_bp = Blueprint("recommend", __name__)

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "recommend_prompt.txt")

FALLBACK_RESPONSE = {
    "recommendations": [
        {
            "action_type": "Immediate",
            "description": "Manual review required — AI service is temporarily unavailable.",
            "priority": "High",
            "expected_outcome": "Findings reviewed by auditor directly",
            "owner": "Audit Team Lead",
        }
    ],
    "is_fallback": True,
}


def load_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    # Required field validation
    required = ["item_name", "department", "risk_level", "compliance_status", "description"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    # Sanitise inputs
    for field in ["item_name", "department", "description", "observations"]:
        if data.get(field):
            cleaned, suspicious = sanitise_input(str(data[field]))
            if suspicious:
                return jsonify({"error": f"Invalid input detected in field: {field}"}), 400
            data[field] = cleaned

    # Build prompt
    try:
        prompt = load_prompt().format(
            item_name=data.get("item_name", ""),
            department=data.get("department", ""),
            risk_level=data.get("risk_level", ""),
            compliance_status=data.get("compliance_status", ""),
            description=data.get("description", ""),
            observations=data.get("observations", "None provided"),
        )
    except Exception as e:
        return jsonify({"error": f"Failed to load prompt: {str(e)}"}), 500

    # Call Groq
    try:
        messages = [{"role": "user", "content": prompt}]
        raw = call_groq(messages, temperature=0.4, max_tokens=1000)
        raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        result = json.loads(raw)

        recs = result.get("recommendations", [])
        if not isinstance(recs, list) or len(recs) == 0:
            raise ValueError("Invalid recommendations format")

        result["is_fallback"] = False

    except Exception:
        result = FALLBACK_RESPONSE.copy()

    result["generated_at"] = datetime.now(timezone.utc).isoformat()
    return jsonify(result), 200