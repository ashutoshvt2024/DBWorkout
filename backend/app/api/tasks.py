from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.task import Task

tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_blueprint.route("/", methods=["POST"])
def create_task():
    """
    Create a new task.
    """
    session = SessionLocal()
    try:
        data = request.json

        # Validate input
        required_fields = ["session_id", "question_text", "solution_query", "category"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Create a new task
        task = Task(
            session_id=data["session_id"],
            question_text=data["question_text"],
            solution_query=data["solution_query"],
            category=data["category"]
        )
        session.add(task)
        session.commit()
        return jsonify({"message": "Task created successfully!", "task_id": task.task_id}), 201

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@tasks_blueprint.route("/", methods=["GET"])
def get_tasks():
    """
    Fetch all tasks for a given session.
    """
    session = SessionLocal()
    try:
        session_id = request.args.get("session_id")
        if not session_id:
            return jsonify({"error": "Session ID is required"}), 400

        tasks = session.query(Task).filter(Task.session_id == session_id).all()
        task_list = [
            {
                "task_id": task.task_id,
                "question_text": task.question_text,
                "solution_query": task.solution_query,
                "category": task.category,
            }
            for task in tasks
        ]
        return jsonify({"tasks": task_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@tasks_blueprint.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """
    Update an existing task.
    """
    session = SessionLocal()
    try:
        data = request.json
        task = session.query(Task).filter(Task.task_id == task_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        # Update fields
        task.question_text = data.get("question_text", task.question_text)
        task.solution_query = data.get("solution_query", task.solution_query)
        task.category = data.get("category", task.category)

        session.commit()
        return jsonify({"message": "Task updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@tasks_blueprint.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """
    Delete a task by ID.
    """
    session = SessionLocal()
    try:
        task = session.query(Task).filter(Task.task_id == task_id).first()
        if not task:
            return jsonify({"error": "Task not found"}), 404

        session.delete(task)
        session.commit()
        return jsonify({"message": "Task deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()