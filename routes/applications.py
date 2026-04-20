from flask import jsonify, request, Blueprint
from werkzeug.exceptions import NotFound, BadRequest
from bson import ObjectId
from db import get_collection

applications_bp = Blueprint("applications", __name__)

# כל המשרות
# כל המשרות + פילרטר לפי סטטוס
@applications_bp.route('/applications', methods=['GET'])
def get_applications():
    col = get_collection("applications")
    # אם יש query param של status - מסנן
    status = request.args.get("status")
    query = {}
    if status:
        query["status"] = status
    apps = list(col.find(query))
    for a in apps:
        a["_id"] = str(a["_id"])
    return jsonify(apps)


# משרה בודדת
@applications_bp.route('/applications/<id>', methods=['GET'])
def get_application(id):
    col = get_collection("applications")
    try:
        app = col.find_one({"_id": ObjectId(id)})
    except:
        raise BadRequest("invalid id format")
    if not app:
        raise NotFound(f"application {id} not found")
    app["_id"] = str(app["_id"])
    return jsonify(app)

# יצירת משרה חדשה
@applications_bp.route('/applications', methods=['POST'])
def create_application():
    col = get_collection("applications")
    if not request.is_json:
        raise BadRequest("request body must be JSON")
    data = request.get_json()
    if "company" not in data or "position" not in data:
        raise BadRequest("missing company or position")
    if not data["company"].strip() or not data["position"].strip():
        raise BadRequest("company and position cant be empty")
    new_app = {
        "company": data["company"].strip(),
        "position": data["position"].strip(),
        "status": "applied",
        "source": data.get("source", ""),
        "notes": data.get("notes", ""),
        "events": []
    }
    col.insert_one(new_app)
    new_app["_id"] = str(new_app["_id"])
    return jsonify(new_app), 201

# עדכון משרה
@applications_bp.route('/applications/<id>', methods=['PUT'])
def update_application(id):
    col = get_collection("applications")
    try:
        app = col.find_one({"_id": ObjectId(id)})
    except:
        raise BadRequest("invalid id")
    if not app:
        raise NotFound("application not found")
    data = request.get_json()
    if not data:
        raise BadRequest("no data provided")
    allowed = ["company", "position", "status", "source", "notes"]
    update_fields = {}
    for field in allowed:
        if field in data:
            update_fields[field] = data[field]
    if not update_fields:
        raise BadRequest("no valid fields to update")
    col.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
    updated = col.find_one({"_id": ObjectId(id)})
    updated["_id"] = str(updated["_id"])
    return jsonify(updated)

# מחיקת משרה
@applications_bp.route('/applications/<id>', methods=['DELETE'])
def delete_application(id):
    col = get_collection("applications")
    try:
        result = col.delete_one({"_id": ObjectId(id)})
    except:
        raise BadRequest("invalid id")
    if result.deleted_count == 0:
        raise NotFound("not found")
    return jsonify({"message": "deleted successfuly"}), 200

# הוספת event למשרה - הlist הפנימי
@applications_bp.route('/applications/<id>/events', methods=['POST'])
def add_event(id):
    col = get_collection("applications")
    try:
        app = col.find_one({"_id": ObjectId(id)})
    except:
        raise BadRequest("invalid id")
    if not app:
        raise NotFound("application not found")
    data = request.get_json()
    if not data or "type" not in data:
        raise BadRequest("missing event type")
    event = {
        "event_id": str(ObjectId()),
        "type": data["type"],
        "note": data.get("note", ""),
        "date": data.get("date", "")
    }
    col.update_one(
        {"_id": ObjectId(id)},
        {"$push": {"events": event}}
    )
    updated = col.find_one({"_id": ObjectId(id)})
    updated["_id"] = str(updated["_id"])
    return jsonify(updated), 201
