from flask import Blueprint, request, jsonify
from app.services.submission_service import (
    create_submission,
    list_submissions,
    get_submission_by_id,
    evaluate_submission,
    update_submission_correctness
)
from app.services.task_service import get_task_by_id
from app.utils.query_executor import validate_query

submissions_blueprint = Blueprint("submissions", __name__)

# Submit a task solution
@submissions_blueprint.route("/submissions", methods=["POST"])
def submit():
    data = request.json
    try:
        new_submission = create_submission(data)
        return jsonify({"message": "Submission created successfully", "submission": new_submission}), 201
    except Exception as e:
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