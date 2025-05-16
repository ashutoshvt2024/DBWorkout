from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.services.course_service import (
    create_course, 
    get_courses, 
    get_course_by_id, 
    update_course, 
    delete_course, 
    get_enrolled_courses
)
import logging
import json

# ✅ Initialize Blueprint
course_blueprint = Blueprint("courses", __name__)
logging.basicConfig(level=logging.INFO)

# ✅ Utility function for extracting JWT user
def get_current_user():
    identity = get_jwt_identity()
    try:
        # If identity is a JSON string, parse it
        identity = json.loads(identity)
    except json.JSONDecodeError:
        pass  # If it's not JSON, assume it's already a dictionary

    return identity

# ---------------------- CREATE COURSE (PROFESSORS ONLY) ----------------------
@course_blueprint.route("/courses", methods=["POST"])
@jwt_required()
def create():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON or no data provided"}), 400

    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can create courses"}), 403

    course_name = data.get("course_name")
    if not course_name or not isinstance(course_name, str):
        return jsonify({"error": "course_name must be a non-empty string"}), 400
    
    try:
        data["professor_id"] = current_user["user_id"]
        new_course = create_course(data)
        return jsonify({"message": "Course created successfully", "course": new_course}), 201
    except Exception as e:
        logging.error(f"Error creating course: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ---------------------- LIST COURSES (PROFESSORS SEE THEIR COURSES, STUDENTS SEE ENROLLED) ----------------------
@course_blueprint.route("/courses", methods=["GET"])
@jwt_required()
def list_courses():
    current_user = get_current_user()

    try:
        if current_user["role"] == "professor":
            courses = get_courses(professor_id=current_user["user_id"])
        elif current_user["role"] == "student":
            courses = get_courses(student_id=current_user["user_id"])
        else:
            return jsonify({"error": "Invalid role"}), 403

        return jsonify({"courses": courses}), 200
    except Exception as e:
        logging.error(f"Error listing courses: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ---------------------- FETCH COURSE DETAILS ----------------------
@course_blueprint.route("/courses/<int:course_id>", methods=["GET"])
@jwt_required()
def get_course(course_id):
    try:
        course = get_course_by_id(course_id)
        if not course:
            return jsonify({"error": "Course not found"}), 404
        return jsonify({"course": course}), 200
    except Exception as e:
        logging.error(f"Error fetching course: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ---------------------- UPDATE COURSE (PROFESSORS ONLY) ----------------------
@course_blueprint.route("/courses/<int:course_id>", methods=["PUT"])
@jwt_required()
def update(course_id):
    data = request.json
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can update courses"}), 403

    try:
        updated_course = update_course(course_id, data)
        return jsonify({"message": "Course updated successfully", "course": updated_course}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logging.error(f"Error updating course: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ---------------------- DELETE COURSE (PROFESSORS ONLY) ----------------------
@course_blueprint.route("/courses/<int:course_id>", methods=["DELETE"])
@jwt_required()
def delete(course_id):
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can delete courses"}), 403

    try:
        delete_course(course_id)
        return jsonify({"message": "Course deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logging.error(f"Error deleting course: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ---------------------- FETCH ENROLLED COURSES (STUDENTS ONLY) ----------------------
@course_blueprint.route("/courses/enrolled", methods=["GET"])
@jwt_required()
def get_enrolled_courses_route():
    current_user = get_current_user()

    if current_user["role"] != "student":
        return jsonify({"error": "Unauthorized - Only students can access enrolled courses"}), 403

    try:
        courses = get_enrolled_courses(current_user["user_id"])
        return jsonify({"courses": courses}), 200
    except Exception as e:
        logging.error(f"Error fetching enrolled courses: {str(e)}")
        return jsonify({"error": str(e)}), 500