from flask import Blueprint, jsonify

describe_bp = Blueprint("describe", __name__)

@describe_bp.route("/describe", methods=["POST"])
def describe():
    return jsonify({"message": "Coming on Day 3"}), 501