from app.db.models.assignment import Assignment
from app.db.session import SessionLocal

# Assign a task to students
def create_assignment(data):
    session = SessionLocal()
    try:
        task_id = data.get("task_id")
        student_id = data.get("student_id")
        assigned_at = data.get("assigned_at")

        if not task_id or not student_id:
            raise ValueError("task_id and student_id are required")

        new_assignment = Assignment(
            task_id=task_id,
            student_id=student_id,
            assigned_at=assigned_at,
        )
        session.add(new_assignment)
        session.commit()

        return {
            "assignment_id": new_assignment.assignment_id,
            "task_id": new_assignment.task_id,
            "student_id": new_assignment.student_id,
            "assigned_at": new_assignment.assigned_at,
        }
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# List all assignments for a specific course or task
def list_assignments(course_id=None, task_id=None):
    session = SessionLocal()
    try:
        query = session.query(Assignment)
        if course_id:
            query = query.filter(Assignment.task.has(course_id=course_id))
        if task_id:
            query = query.filter(Assignment.task_id == task_id)

        assignments = query.all()
        return [
            {
                "assignment_id": a.assignment_id,
                "task_id": a.task_id,
                "student_id": a.student_id,
                "assigned_at": a.assigned_at,
                "status": a.status,
                "grade": a.grade,
            }
            for a in assignments
        ]
    finally:
        session.close()

# Fetch assignment details
def get_assignment_by_id(assignment_id):
    session = SessionLocal()
    try:
        assignment = session.query(Assignment).get(assignment_id)
        if not assignment:
            raise ValueError("Assignment not found")

        return {
            "assignment_id": assignment.assignment_id,
            "task_id": assignment.task_id,
            "student_id": assignment.student_id,
            "assigned_at": assignment.assigned_at,
            "status": assignment.status,
            "grade": assignment.grade,
        }
    finally:
        session.close()

# Update assignment details
def update_assignment(assignment_id, data):
    session = SessionLocal()
    try:
        assignment = session.query(Assignment).get(assignment_id)
        if not assignment:
            raise ValueError("Assignment not found")

        assignment.status = data.get("status", assignment.status)
        assignment.grade = data.get("grade", assignment.grade)
        session.commit()

        return {
            "assignment_id": assignment.assignment_id,
            "task_id": assignment.task_id,
            "student_id": assignment.student_id,
            "assigned_at": assignment.assigned_at,
            "status": assignment.status,
            "grade": assignment.grade,
        }
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Remove an assignment
def delete_assignment(assignment_id):
    session = SessionLocal()
    try:
        assignment = session.query(Assignment).get(assignment_id)
        if not assignment:
            raise ValueError("Assignment not found")

        session.delete(assignment)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()