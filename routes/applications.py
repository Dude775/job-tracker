from flask import jsonify, request, Blueprint
from db import get_collection
from bson import ObjectId

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

# get one by id
@applications_bp.route('/applications/<id>', methods=['GET'])
def get_application(id):
    col = get_collection("applications")
    try:
        app = col.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "invalid id format"}), 400
    if not app:
        return jsonify({"error": "application not found"}), 404
    app["_id"] = str(app["_id"])
    return jsonify(app)

# update
@applications_bp.route('/applications/<id>', methods=['PUT'])
def update_application(id):
    col = get_collection("applications")
    try:
        app = col.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "invalid id"}), 400
    if not app:
        return jsonify({"error": "not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 400
    allowed = ["company", "position", "status", "source", "notes"]
    update_fields = {}
    for field in allowed:
        if field in data:
            update_fields[field] = data[field]
    if not update_fields:
        return jsonify({"error": "no valid fields"}), 400
    col.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
    updated = col.find_one({"_id": ObjectId(id)})
    updated["_id"] = str(updated["_id"])
    return jsonify(updated)
