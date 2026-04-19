from flask import jsonify, Blueprint

applications_bp = Blueprint("applications", __name__)

# TODO: add all CRUD endpoints
@applications_bp.route('/applications', methods=['GET'])
def get_applications():
    return jsonify([])  # empty for now
