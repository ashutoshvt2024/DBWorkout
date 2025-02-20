from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.task_service import (
    create_task,
    list_tasks,
    get_task_by_id,
    update_task,
    delete_task,
    professor_owns_course
)
import logging
import json

# ✅ Initialize Blueprint
tasks_blueprint = Blueprint("tasks", __name__)
logging.basicConfig(level=logging.INFO)

# ✅ Utility function for extracting JWT user
def get_current_user():
    identity = get_jwt_identity()
    try:
        identity = json.loads(identity)
    except json.JSONDecodeError:
        pass
    return identity

# ---------------------- CREATE TASK (PROFESSORS ONLY) ----------------------
@tasks_blueprint.route("/tasks", methods=["POST"])
@jwt_required()
def create_task_route():
    data = request.json
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can create tasks"}), 403

    required_fields = ["task_title", "task_description", "course_id", "session_id", "schema_id", "difficulty", "deadline", "correct_answer"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Ensure difficulty is valid
    if data["difficulty"] not in ["easy", "medium", "hard"]:
        return jsonify({"error": "Invalid difficulty level. Choose from 'easy', 'medium', 'hard'"}), 400

    # Check if professor owns the course
    if not professor_owns_course(current_user["user_id"], data["course_id"]):
        return jsonify({"error": "Unauthorized - You do not own this course"}), 403

    try:
        new_task = create_task(data)
        return jsonify({"message": "Task created successfully", "task": new_task}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logging.error(f"Error creating task: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

# ---------------------- LIST TASKS (STUDENTS & PROFESSORS) ----------------------
@tasks_blueprint.route("/tasks", methods=["GET"])
@jwt_required()
def list_all_tasks():
    course_id = request.args.get("course_id")
    session_id = request.args.get("session_id")
    current_user = get_current_user()

    try:
        tasks = list_tasks(course_id, session_id)

        # Hide correct_answer for students
        if current_user["role"] == "student":
            for task in tasks:
                task.pop("correct_answer", None)

        return jsonify({"tasks": tasks}), 200
    except Exception as e:
        logging.error(f"Error listing tasks: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ---------------------- FETCH TASK DETAILS (STUDENTS & PROFESSORS) ----------------------
@tasks_blueprint.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task_details(task_id):
    current_user = get_current_user()

    try:
        task = get_task_by_id(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        # Hide correct_answer for students
        if current_user["role"] == "student":
            task.pop("correct_answer", None)

        return jsonify({"task": task}), 200
    except Exception as e:
        logging.error(f"Error fetching task: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ---------------------- UPDATE TASK (PROFESSORS ONLY) ----------------------
@tasks_blueprint.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task_route(task_id):
    data = request.json
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can update tasks"}), 403

    task = get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    if not professor_owns_course(current_user["user_id"], task["course_id"]):
        return jsonify({"error": "Unauthorized - You do not own this course"}), 403
    
    try:
        updated_task = update_task(task_id, data)
        return jsonify({"message": "Task updated successfully", "task": updated_task}), 200
    except Exception as e:
        logging.error(f"Error updating task: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ---------------------- DELETE TASK (PROFESSORS ONLY) ----------------------
@tasks_blueprint.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task_route(task_id):
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can delete tasks"}), 403

    task = get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    if not professor_owns_course(current_user["user_id"], task["course_id"]):
        return jsonify({"error": "Unauthorized - You do not own this course"}), 403
    
    try:
        delete_task(task_id)
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting task: {str(e)}")
        return jsonify({"error": str(e)}), 500