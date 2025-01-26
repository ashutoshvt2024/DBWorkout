from flask import Blueprint, request, jsonify
from app.services.task_service import (
    create_task,
    list_tasks,
    get_task_by_id,
    update_task,
    delete_task,
)

tasks_blueprint = Blueprint("tasks", __name__)

# Create a new task in a session
@tasks_blueprint.route("/tasks", methods=["POST"])
def create():
    data = request.json
    try:
        new_task = create_task(data)
        return jsonify({"message": "Task created successfully", "task": new_task}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# List all tasks for a specific course or session
@tasks_blueprint.route("/tasks", methods=["GET"])
def list_all():
    course_id = request.args.get("course_id")
    session_id = request.args.get("session_id")
    try:
        tasks = list_tasks(course_id, session_id)
        return jsonify({"tasks": tasks}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Fetch task details (includes correct answer for professors)
@tasks_blueprint.route("/tasks/<int:task_id>", methods=["GET"])
def get_details(task_id):
    try:
        task = get_task_by_id(task_id)
        return jsonify({"task": task}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# Update task details
@tasks_blueprint.route("/tasks/<int:task_id>", methods=["PUT"])
def update(task_id):
    data = request.json
    try:
        updated_task = update_task(task_id, data)
        return jsonify({"message": "Task updated successfully", "task": updated_task}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a task
@tasks_blueprint.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete(task_id):
    try:
        delete_task(task_id)
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400