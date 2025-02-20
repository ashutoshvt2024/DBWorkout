from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.session_service import (
    create_session,
    get_sessions,
    get_session_by_id,
    update_session,
    delete_session,
)
import json
import logging

session_blueprint = Blueprint("sessions", __name__)
logging.basicConfig(level=logging.INFO)

# ✅ Utility function for extracting JWT user
def get_current_user():
    identity = get_jwt_identity()
    try:
        identity = json.loads(identity)
    except json.JSONDecodeError:
        pass
    return identity

# ---------------------- CREATE SESSION (PROFESSORS ONLY) ----------------------
@session_blueprint.route("/sessions", methods=["POST"])
@jwt_required()
def create_session_route():
    data = request.json
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can create sessions"}), 403

    try:
        new_session = create_session(data, current_user["user_id"])  # Ensure professor ID is validated
        return jsonify({"message": "Session created successfully", "session": new_session}), 201
    except Exception as e:
        logging.error(f"Error creating session: {str(e)}")
        return jsonify({"error": str(e)}), 400

# ---------------------- LIST SESSIONS (STUDENTS & PROFESSORS) ----------------------
@session_blueprint.route("/sessions", methods=["GET"])
@jwt_required()
def list_sessions_route():
    course_id = request.args.get("course_id")
    current_user = get_current_user()

    try:
        sessions = get_sessions(course_id, current_user["user_id"], current_user["role"])
        return jsonify({"sessions": sessions}), 200
    except Exception as e:
        logging.error(f"Error listing sessions: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ---------------------- GET SESSION DETAILS (STUDENTS & PROFESSORS) ----------------------
@session_blueprint.route("/sessions/<int:session_id>", methods=["GET"])
@jwt_required()
def get_session_details(session_id):
    try:
        session = get_session_by_id(session_id)
        if not session:
            return jsonify({"error": "Session not found"}), 404
        return jsonify({"session": session}), 200
    except Exception as e:
        logging.error(f"Error fetching session: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ---------------------- UPDATE SESSION (PROFESSORS ONLY) ----------------------
@session_blueprint.route("/sessions/<int:session_id>", methods=["PUT"])
@jwt_required()
def update_session_route(session_id):
    data = request.json
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can update sessions"}), 403

    try:
        updated_session = update_session(session_id, data, current_user["user_id"])
        return jsonify({"message": "Session updated successfully", "session": updated_session}), 200
    except Exception as e:
        logging.error(f"Error updating session: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ---------------------- DELETE SESSION (PROFESSORS ONLY) ----------------------
@session_blueprint.route("/sessions/<int:session_id>", methods=["DELETE"])
@jwt_required()
def delete_session_route(session_id):
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can delete sessions"}), 403

    try:
        delete_session(session_id, current_user["user_id"])
        return jsonify({"message": "Session deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting session: {str(e)}")
        return jsonify({"error": str(e)}), 500