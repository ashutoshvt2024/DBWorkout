from app.db.models.task import Task
from app.db.models.course import Course
from app.db.session import SessionLocal
from app.db.models.schema import Schema
from sqlalchemy.orm import Session
import logging
# Create a new task
def create_task(data):
    session = SessionLocal()
    try:
        logging.info(f"Creating task with data: {data}")
        task_title = data.get("task_title")
        task_description = data.get("task_description")
        course_id = data.get("course_id")
        session_id = data.get("session_id")
        schema_id = data.get("schema_id")
        correct_answer = data.get("correct_answer")
        difficulty = data.get("difficulty", "medium")
        tags = data.get("tags")
        deadline = data.get("deadline")

        # Validate required fields
        if not task_title or not task_description or not course_id or not session_id or not schema_id or not correct_answer:
            raise ValueError("Missing required fields for task creation")

        # Check if the provided schema_id exists
        schema_exists = session.query(Schema).filter(Schema.schema_id == schema_id).first()
        if not schema_exists:
            raise ValueError(f"Schema with ID {schema_id} does not exist.")

        # Create the new task
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
        logging.info(f"Task created successfully with ID: {new_task.task_id}")
        return new_task.to_dict()
    except Exception as e:
        session.rollback()
        logging.error(f"Error creating task: {e}")
        raise e
    finally:
        session.close()


# Fetch task details by ID
def get_task_by_id(task_id):
    session = SessionLocal()
    try:
        task = session.query(Task).get(task_id)
        if not task:
            raise ValueError("Task not found")
        return task.to_dict()
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

        # Update the published status if provided
        if "published" in data:
            task.published = data["published"]

        session.commit()
        return task.to_dict()
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

# Check if a professor owns a course
def professor_owns_course(professor_id: int, course_id: int) -> bool:
    """Check if the professor owns the given course_id."""
    session = SessionLocal()
    try:
        return session.query(Course).filter(
            Course.course_id == course_id,
            Course.professor_id == professor_id
        ).first() is not None
    except Exception as e:
        session.rollback()
        print(f"Error checking course ownership: {str(e)}")
        return False
    finally:
        session.close()

def publish_task(task_id):
    session = SessionLocal()
    try:
        # Fetch the task by ID
        task = session.query(Task).get(task_id)
        if not task:
            raise ValueError("Task not found")

        # Mark the task as published
        task.published = True
        session.commit()

        return task.to_dict()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def list_tasks(course_id=None, session_id=None, include_unpublished=False):
    session = SessionLocal()
    try:
        query = session.query(Task)
        if course_id:
            query = query.filter(Task.course_id == course_id)
        if session_id:
            query = query.filter(Task.session_id == session_id)

        # Filter out unpublished tasks unless explicitly requested
        if not include_unpublished:
            query = query.filter(Task.published == True)

        tasks = query.all()
        return [task.to_dict(hide_correct_answer=True) for task in tasks]
    finally:
        session.close()