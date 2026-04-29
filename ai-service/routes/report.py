from flask import Blueprint, jsonify

report_bp = Blueprint("report", __name__)

@report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    return jsonify({"message": "Coming on Day 6"}), 501