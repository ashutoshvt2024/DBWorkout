from flask import Blueprint, jsonify, request
from app.db.session import SandboxSessionLocal, SessionLocal
from app.db.models.task import Task
from app.utils.query_executor import execute_and_compare
from app.db.models.submission import Submission

submissions_blueprint = Blueprint("submissions", __name__, url_prefix="/submissions")

@submissions_blueprint.route("/submit", methods=["POST"])
def submit_query():
    """
    Compares a user's query result with the instructor's solution query result within the instructor_schema.
    """
    main_session = SessionLocal()
    sandbox_session = SandboxSessionLocal()
    try:
        data = request.json
        task_id = data["task_id"]
        user_query = data["user_query"]

        # Fetch the task details, including the solution query
        task = main_session.query(Task).filter(Task.task_id == task_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        expected_query = task.solution_query

        # Execute and compare results within the instructor_schema
        comparison_result = execute_and_compare(
            user_query=user_query,
            solution_query=f"SET search_path TO instructor_schema; {expected_query}",
            sandbox_session=sandbox_session
        )

        # Save the submission result
        submission = Submission(
            task_id=task_id,
            user_id=data.get("user_id"),  # Ensure user_id is passed in the request
            submitted_query=user_query,
            is_correct=comparison_result["is_correct"]
        )
        main_session.add(submission)
        main_session.commit()

        # Return comparison results
        if comparison_result["is_correct"]:
            return jsonify({
                "is_correct": True,
                "message": "Query is correct!",
                "expected_result": comparison_result["expected_result"],
                "user_result": comparison_result["user_result"]
            }), 200
        else:
            return jsonify({
                "is_correct": False,
                "message": "Query results do not match",
                "expected_result": comparison_result["expected_result"],
                "user_result": comparison_result["user_result"]
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        main_session.close()
        sandbox_session.close()