from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.course_service import (
    create_course, 
    get_courses, 
    get_course_by_id, 
    update_course, 
    delete_course, 
    get_enrolled_courses
)
import json

course_blueprint = Blueprint("courses", __name__)

# Create a new course
@course_blueprint.route("/courses", methods=["POST"])
@jwt_required()
def create():
    data = request.json
    current_user = json.loads(get_jwt_identity())  # Extract the user from the JWT token

    # Validate user role
    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized"}), 403

    try:
        # Validate course_name
        if "course_name" not in data or not isinstance(data["course_name"], str):
            return jsonify({"error": "course_name must be a non-empty string"}), 400
        
        # Dynamically add professor_id from the logged-in user
        data["professor_id"] = current_user["user_id"]
        new_course = create_course(data)
        return jsonify({"message": "Course created successfully", "course": new_course}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# List all courses dynamically based on user role
@course_blueprint.route("/courses", methods=["GET"])
@jwt_required()
def list_courses():
    current_user = json.loads(get_jwt_identity())  # Extract the user from the JWT token

    try:
        # Determine the user role and fetch courses accordingly
        if current_user["role"] == "professor":
            professor_id = current_user["user_id"]
            courses = get_courses(professor_id=professor_id)
        elif current_user["role"] == "student":
            student_id = current_user["user_id"]
            courses = get_courses(student_id=student_id)
        else:
            return jsonify({"error": "Invalid role"}), 400

        return jsonify({"courses": courses}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Fetch course details
@course_blueprint.route("/courses/<int:course_id>", methods=["GET"])
@jwt_required()
def get_course(course_id):
    try:
        course = get_course_by_id(course_id)
        return jsonify({"course": course}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# Update course information
@course_blueprint.route("/courses/<int:course_id>", methods=["PUT"])
@jwt_required()
def update(course_id):
    data = request.json
    current_user = json.loads(get_jwt_identity())  # Extract the user from the JWT token

    # Validate user role
    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized"}), 403

    try:
        updated_course = update_course(course_id, data)
        return jsonify({"message": "Course updated successfully", "course": updated_course}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a course
@course_blueprint.route("/courses/<int:course_id>", methods=["DELETE"])
@jwt_required()
def delete(course_id):
    current_user = json.loads(get_jwt_identity())  # Extract the user from the JWT token

    # Validate user role
    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized"}), 403

    try:
        delete_course(course_id)
        return jsonify({"message": "Course deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Fetch enrolled courses for a student
@course_blueprint.route("/courses/enrolled", methods=["GET"])
@jwt_required()
def get_enrolled_courses_route():
    current_user = json.loads(get_jwt_identity())  # Extract the user from the JWT token

    # Validate user role
    if current_user["role"] != "student":
        return jsonify({"error": "Unauthorized"}), 403

    try:
        student_id = current_user["user_id"]
        courses = get_enrolled_courses(student_id)
        return jsonify({"courses": courses}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400