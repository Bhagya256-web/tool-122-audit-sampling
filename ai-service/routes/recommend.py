from flask import Blueprint, jsonify

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    return jsonify({"message": "Coming on Day 4"}), 501