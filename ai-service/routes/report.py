import json
import os
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from services.groq_client import call_groq
from services.sanitiser import sanitise_input

report_bp = Blueprint("report", __name__)

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "report_prompt.txt")

FALLBACK_RESPONSE = {
    "title": "Audit Report — Unavailable",
    "executive_summary": "AI service is temporarily unavailable. Please try again later.",
    "overview": "Report generation failed. Manual review required.",
    "key_items": [],
    "recommendations": [],
    "conclusion": "Please contact the audit team for a manual report.",
    "audit_opinion": "Disclaimer",
    "is_fallback": True,
}


def load_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


@report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    # Required field validation
    required = ["audit_title", "department", "period", "sample_size"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    # Sanitise inputs
    for field in ["audit_title", "department", "period", "findings", "risk_summary"]:
        if data.get(field):
            cleaned, suspicious = sanitise_input(str(data[field]))
            if suspicious:
                return jsonify({"error": f"Invalid input in field: {field}"}), 400
            data[field] = cleaned

    # Build prompt
    try:
        prompt = load_prompt().format(
            audit_title=data.get("audit_title", ""),
            department=data.get("department", ""),
            period=data.get("period", ""),
            sample_size=data.get("sample_size", ""),
            items_reviewed=data.get("items_reviewed", "Not specified"),
            risk_summary=data.get("risk_summary", "Not provided"),
            findings=data.get("findings", "Not provided"),
        )
    except Exception as e:
        return jsonify({"error": f"Failed to load prompt: {str(e)}"}), 500

    # Call Groq
    try:
        messages = [{"role": "user", "content": prompt}]
        raw = call_groq(messages, temperature=0.3, max_tokens=1500)
        raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        result = json.loads(raw)
        result["is_fallback"] = False

    except Exception:
        result = FALLBACK_RESPONSE.copy()

    result["generated_at"] = datetime.now(timezone.utc).isoformat()
    return jsonify(result), 200