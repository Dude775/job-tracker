from flask import jsonify, request, Blueprint
from db import get_collection

applications_bp = Blueprint("applications", __name__)

# get all
@applications_bp.route('/applications', methods=['GET'])
def get_applications():
    col = get_collection("applications")
    apps = list(col.find())
    for a in apps:
        a["_id"] = str(a["_id"])
    return jsonify(apps)

# add new
@applications_bp.route('/applications', methods=['POST'])
def create_application():
    col = get_collection("applications")
    data = request.get_json()
    if not data or "company" not in data or "position" not in data:
        return jsonify({"error": "missing company or position"}), 400
    new_app = {
        "company": data["company"].strip(),
        "position": data["position"].strip(),
        "status": "applied",
        "events": []
    }
    col.insert_one(new_app)
    new_app["_id"] = str(new_app["_id"])
    return jsonify(new_app), 201
