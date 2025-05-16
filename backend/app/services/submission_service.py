from app.db.models.submission import Submission
from app.db.models.task import Task
from app.db.session import SessionLocal
from sqlalchemy.orm import joinedload
from app.db.models.schema import Schema  # Import the Schema model
# Submit a task solution
def create_submission(data):
    session = SessionLocal()
    try:
        assignment_id = data.get("assignment_id")
        submitted_query = data.get("submitted_query")
        time_taken = data.get("time_taken")

        if not assignment_id or not submitted_query or time_taken is None:
            raise ValueError("assignment_id, submitted_query, and time_taken are required")

        new_submission = Submission(
            assignment_id=assignment_id,
            submitted_query=submitted_query,
            is_correct=False,  # Initially, correctness is not determined
            time_taken=time_taken,
        )
        session.add(new_submission)
        session.commit()

        return {
            "submission_id": new_submission.submission_id,
            "assignment_id": new_submission.assignment_id,
            "submitted_query": new_submission.submitted_query,
            "is_correct": new_submission.is_correct,
            "time_taken": new_submission.time_taken,
            "submitted_at": new_submission.submitted_at,
        }
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# List all submissions for a task or student
def list_submissions(task_id=None, student_id=None):
    session = SessionLocal()
    try:
        query = session.query(Submission)
        if task_id:
            query = query.filter(Submission.assignment.has(task_id=task_id))
        if student_id:
            query = query.filter(Submission.assignment.has(student_id=student_id))

        submissions = query.all()
        return [
            {
                "submission_id": s.submission_id,
                "assignment_id": s.assignment_id,
                "submitted_query": s.submitted_query,
                "is_correct": s.is_correct,
                "submitted_at": s.submitted_at,
            }
            for s in submissions
        ]
    finally:
        session.close()

# Fetch submission details
def get_submission_by_id(submission_id):
    session = SessionLocal()
    try:
        submission = session.query(Submission).get(submission_id)
        if not submission:
            raise ValueError("Submission not found")

        return {
            "submission_id": submission.submission_id,
            "assignment_id": submission.assignment_id,
            "submitted_query": submission.submitted_query,
            "is_correct": submission.is_correct,
            "submitted_at": submission.submitted_at,
        }
    finally:
        session.close()

# Evaluate a submission
def evaluate_submission(submission_id):
    session = SessionLocal()
    try:
        submission = session.query(Submission).get(submission_id)
        if not submission:
            raise ValueError("Submission not found")

        task = session.query(Task).filter(Task.task_id == submission.assignment.task_id).first()
        if not task:
            raise ValueError("Task not found for the submission")

        # Evaluate correctness
        submission.is_correct = submission.submitted_query.strip().lower() == task.correct_answer.strip().lower()
        session.commit()

        return {"is_correct": submission.is_correct}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update_submission_correctness(submission_id, is_correct):
    session = SessionLocal()
    try:
        submission = session.query(Submission).get(submission_id)
        if not submission:
            raise ValueError("Submission not found")

        submission.is_correct = is_correct
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()



def get_task_by_id(task_id):
    session = SessionLocal()
    try:
        # Fetch the task and eagerly load the schema relationship
        task = session.query(Task).options(joinedload(Task.schema)).filter(Task.task_id == task_id).first()
        if not task:
            return None

        # Access the schema_name using the relationship
        schema_name = task.schema.schema_name if task.schema else None

        # Return the task details, including schema_name
        return {
            "task_id": task.task_id,
            "task_title": task.task_title,
            "task_description": task.task_description,
            "course_id": task.course_id,
            "session_id": task.session_id,
            "schema_id": task.schema_id,
            "schema_name": schema_name,  # Include schema_name
            "correct_answer": task.correct_answer,
            "difficulty": task.difficulty,
            "tags": task.tags,
            "deadline": str(task.deadline),
            "created_at": str(task.created_at),
            "published": task.published,
        }
    finally:
        session.close()