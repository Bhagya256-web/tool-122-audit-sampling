from flask import Blueprint, request, jsonify
from services.ai_service_client import AiServiceClient
from services.sanitiser import sanitise_input

analyse_bp = Blueprint("analyse", __name__)
client = AiServiceClient()


@analyse_bp.route("/analyse", methods=["POST"])
def analyse():
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

    # Call full analysis — handles None gracefully
    result = client.full_analysis(
        item_name=data.get("item_name"),
        department=data.get("department"),
        sample_size=data.get("sample_size"),
        period=data.get("period"),
        notes=data.get("notes", ""),
    )

    return jsonify(result), 200