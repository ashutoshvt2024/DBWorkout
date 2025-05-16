from flask import Blueprint, request, jsonify
from app.db.models import Submission, Assignment
from app.db.session import SessionLocal
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from app.services.submission_service import (
    create_submission,
    list_submissions,
    get_submission_by_id,
    evaluate_submission,
    update_submission_correctness,
    get_task_by_id
)
from app.services.task_service import get_task_by_id
from app.utils.query_executor import validate_query

submissions_blueprint = Blueprint("submissions", __name__)

# Submit a task solution
@submissions_blueprint.route("/submissions", methods=["POST"])
def submit():
    data = request.json
    logging.info(f"Received payload: {data}")  # Debugging: Log the payload
    try:
        assignment_id = data.get("assignment_id")
        submitted_query = data.get("submitted_query")
        time_taken = data.get("time_taken")  # Timer value from frontend

        if not assignment_id or not submitted_query or time_taken is None:
            return jsonify({"error": "assignment_id, submitted_query, and time_taken are required"}), 400

        # Fetch the task details (correct answer and schema)
        task = get_task_by_id(assignment_id)
        logging.info(f"Fetched task: {task}")  # Debugging: Log the task object
        if not task:
            return jsonify({"error": "Task not found"}), 404

        correct_answer = task["correct_answer"]
        schema_name = task["schema_name"]  # Use the schema_name from the task object

        if not schema_name:
            return jsonify({"error": "Schema not found for the task"}), 400

        # Validate the query
        validation_result = validate_query(submitted_query, correct_answer, schema_name)

        # If the query is correct, save the submission and stop the timer
        is_correct = validation_result["is_correct"]
        feedback = validation_result["feedback"]

        # Save the submission
        new_submission = create_submission({
            "assignment_id": assignment_id,
            "submitted_query": submitted_query,
            "time_taken": time_taken if is_correct else None,  # Only save time if correct
            "is_correct": is_correct,
        })

        # Return the validation result and feedback
        return jsonify({
            "message": "Submission evaluated successfully",
            "submission": new_submission,
            "is_correct": is_correct,
            "feedback": feedback,
        }), 200
    except Exception as e:
        logging.error(f"Error in submit endpoint: {e}")  # Debugging: Log the error
        return jsonify({"error": str(e)}), 400

# List all submissions for a task or student
@submissions_blueprint.route("/submissions", methods=["GET"])
def list_all():
    task_id = request.args.get("task_id")
    student_id = request.args.get("student_id")
    try:
        submissions = list_submissions(task_id, student_id)
        return jsonify({"submissions": submissions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Fetch submission details
@submissions_blueprint.route("/submissions/<int:submission_id>", methods=["GET"])
def get_details(submission_id):
    try:
        submission = get_submission_by_id(submission_id)
        return jsonify({"submission": submission}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# Evaluate a submission
@submissions_blueprint.route("/submissions/<int:submission_id>/evaluate", methods=["POST"])
def evaluate(submission_id):
    try:
        # Fetch submission details
        submission = get_submission_by_id(submission_id)
        if not submission:
            return jsonify({"error": "Submission not found"}), 404

        # Extract required details
        submitted_query = submission["submitted_query"]
        assignment_id = submission["assignment_id"]

        # Fetch the task details (correct answer and schema)
        task = get_task_by_id(assignment_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        correct_answer = task["correct_answer"]
        schema_name = task["schema_name"]

        # Validate the query
        validation_result = validate_query(submitted_query, correct_answer, schema_name)

        # Update the submission's correctness in the database
        update_submission_correctness(submission_id, validation_result["is_correct"])

        # Return the validation result
        return jsonify({
            "message": "Submission evaluated successfully",
            "evaluation_result": validation_result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@submissions_blueprint.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    try:
        task_id = request.args.get("task_id")
        if not task_id:
            return jsonify({"error": "task_id is required"}), 400

        session = SessionLocal()
        leaderboard = (
            session.query(Submission.assignment_id, Submission.time_taken, Submission.is_correct)
            .join(Assignment, Submission.assignment_id == Assignment.assignment_id)
            .filter(Assignment.task_id == task_id, Submission.is_correct == True)
            .order_by(Submission.time_taken.asc())
            .all()
        )

        return jsonify([
            {
                "assignment_id": entry.assignment_id,
                "time_taken": entry.time_taken,
                "is_correct": entry.is_correct,
            }
            for entry in leaderboard
        ]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400