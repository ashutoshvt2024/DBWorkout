from app.db.models.task import Task
from app.db.session import SessionLocal

# Create a new task
def create_task(data):
    session = SessionLocal()
    try:
        task_title = data.get("task_title")
        task_description = data.get("task_description")
        course_id = data.get("course_id")
        session_id = data.get("session_id")
        schema_id = data.get("schema_id")
        correct_answer = data.get("correct_answer")
        difficulty = data.get("difficulty", "medium")
        tags = data.get("tags")
        deadline = data.get("deadline")

        if not task_title or not task_description or not course_id or not session_id or not schema_id or not correct_answer:
            raise ValueError("Missing required fields for task creation")

        new_task = Task(
            task_title=task_title,
            task_description=task_description,
            course_id=course_id,
            session_id=session_id,
            schema_id=schema_id,
            correct_answer=correct_answer,
            difficulty=difficulty,
            tags=tags,
            deadline=deadline,
        )
        session.add(new_task)
        session.commit()

        return {
            "task_id": new_task.task_id,
            "task_title": new_task.task_title,
            "task_description": new_task.task_description,
            "course_id": new_task.course_id,
            "session_id": new_task.session_id,
            "schema_id": new_task.schema_id,
            "correct_answer": new_task.correct_answer,
            "difficulty": new_task.difficulty,
            "tags": new_task.tags,
            "deadline": new_task.deadline,
        }
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# List all tasks for a specific course or session
def list_tasks(course_id=None, session_id=None):
    session = SessionLocal()
    try:
        query = session.query(Task)
        if course_id:
            query = query.filter(Task.course_id == course_id)
        if session_id:
            query = query.filter(Task.session_id == session_id)
        tasks = query.all()
        return [
            {
                "task_id": task.task_id,
                "task_title": task.task_title,
                "task_description": task.task_description,
                "course_id": task.course_id,
                "session_id": task.session_id,
                "schema_id": task.schema_id,
                "tags": task.tags,
                "deadline": task.deadline,
            }
            for task in tasks
        ]
    finally:
        session.close()

# Fetch task details by ID
def get_task_by_id(task_id):
    session = SessionLocal()
    try:
        task = session.query(Task).get(task_id)
        if not task:
            raise ValueError("Task not found")
        return {
            "task_id": task.task_id,
            "task_title": task.task_title,
            "task_description": task.task_description,
            "course_id": task.course_id,
            "session_id": task.session_id,
            "schema_id": task.schema_id,
            "correct_answer": task.correct_answer,
            "difficulty": task.difficulty,
            "tags": task.tags,
            "deadline": task.deadline,
        }
    finally:
        session.close()

# Update task details
def update_task(task_id, data):
    session = SessionLocal()
    try:
        task = session.query(Task).get(task_id)
        if not task:
            raise ValueError("Task not found")

        task.task_title = data.get("task_title", task.task_title)
        task.task_description = data.get("task_description", task.task_description)
        task.correct_answer = data.get("correct_answer", task.correct_answer)
        task.difficulty = data.get("difficulty", task.difficulty)
        task.tags = data.get("tags", task.tags)
        task.deadline = data.get("deadline", task.deadline)
        session.commit()

        return {
            "task_id": task.task_id,
            "task_title": task.task_title,
            "task_description": task.task_description,
            "course_id": task.course_id,
            "session_id": task.session_id,
            "schema_id": task.schema_id,
            "correct_answer": task.correct_answer,
            "difficulty": task.difficulty,
            "tags": task.tags,
            "deadline": task.deadline,
        }
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Delete a task
def delete_task(task_id):
    session = SessionLocal()
    try:
        task = session.query(Task).get(task_id)
        if not task:
            raise ValueError("Task not found")

        session.delete(task)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()