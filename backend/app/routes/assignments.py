from flask import Blueprint, request, jsonify
from app.services.assignment_service import (
    create_assignment,
    list_assignments,
    get_assignment_by_id,
    update_assignment,
    delete_assignment,
)

assignment_blueprint = Blueprint("assignments", __name__)

# Assign a task to students
@assignment_blueprint.route("/assignments", methods=["POST"])
def create():
    data = request.json
    try:
        new_assignment = create_assignment(data)
        return jsonify({"message": "Assignment created successfully", "assignment": new_assignment}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# List all assignments for a specific course or task
@assignment_blueprint.route("/assignments", methods=["GET"])
def list_all():
    course_id = request.args.get("course_id")
    task_id = request.args.get("task_id")
    try:
        assignments = list_assignments(course_id, task_id)
        return jsonify({"assignments": assignments}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Fetch assignment details
@assignment_blueprint.route("/assignments/<int:assignment_id>", methods=["GET"])
def get_details(assignment_id):
    try:
        assignment = get_assignment_by_id(assignment_id)
        return jsonify({"assignment": assignment}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# Update assignment details
@assignment_blueprint.route("/assignments/<int:assignment_id>", methods=["PUT"])
def update(assignment_id):
    data = request.json
    try:
        updated_assignment = update_assignment(assignment_id, data)
        return jsonify({"message": "Assignment updated successfully", "assignment": updated_assignment}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Remove an assignment
@assignment_blueprint.route("/assignments/<int:assignment_id>", methods=["DELETE"])
def delete(assignment_id):
    try:
        delete_assignment(assignment_id)
        return jsonify({"message": "Assignment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400