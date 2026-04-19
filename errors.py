from flask import Blueprint, jsonify

errors_bp = Blueprint("errors", __name__)

# TODO: add more handlers as we need them
@errors_bp.app_errorhandler(404)
def handle_not_found(e):
    return jsonify({"error": "not found", "status": 404}), 404
