from flask import Blueprint, jsonify
from werkzeug.exceptions import NotFound, BadRequest, HTTPException

errors_bp = Blueprint("errors", __name__)

# 404 - לא נמצא
@errors_bp.app_errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({
        "error": "not found",
        "message": str(e.description),
        "status": 404
    }), 404

# 400 - בקשה לא תקינה
@errors_bp.app_errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({
        "error": "bad request",
        "message": str(e.description),
        "status": 400
    }), 400

# catch-all ל-HTTP errors - 405 וכו
@errors_bp.app_errorhandler(HTTPException)
def handle_http_error(e):
    return jsonify({
        "error": e.name.lower(),
        "message": e.description,
        "status": e.code
    }), e.code

# 500 - שגיאה כללית
@errors_bp.app_errorhandler(Exception)
def handle_generic_error(e):
    return jsonify({
        "error": "internal server error",
        "message": "something went wrong",
        "status": 500
    }), 500
