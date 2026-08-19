from flask import Blueprint, jsonify


health_bp = Blueprint("health", __name__)


@health_bp.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "message": "Enterprise AI Knowledge Platform API is running"
    }), 200