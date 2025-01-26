from flask import Blueprint, request, jsonify
from app.services.session_service import (
    create_session,
    get_sessions,
    get_session_by_id,
    update_session,
    delete_session,
)

session_blueprint = Blueprint("sessions", __name__)

# Create a new session in a course
@session_blueprint.route("/sessions", methods=["POST"])
def create():
    data = request.json
    try:
        new_session = create_session(data)
        return jsonify({"message": "Session created successfully", "session": new_session}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# List all sessions for a specific course
@session_blueprint.route("/sessions", methods=["GET"])
def list_all():
    course_id = request.args.get("course_id")
    try:
        sessions = get_sessions(course_id)
        return jsonify({"sessions": sessions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Fetch session details
@session_blueprint.route("/sessions/<int:session_id>", methods=["GET"])
def get_details(session_id):
    try:
        session = get_session_by_id(session_id)
        return jsonify({"session": session}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# Update session details
@session_blueprint.route("/sessions/<int:session_id>", methods=["PUT"])
def update(session_id):
    data = request.json
    try:
        updated_session = update_session(session_id, data)
        return jsonify({"message": "Session updated successfully", "session": updated_session}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a session
@session_blueprint.route("/sessions/<int:session_id>", methods=["DELETE"])
def delete(session_id):
    try:
        delete_session(session_id)
        return jsonify({"message": "Session deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400