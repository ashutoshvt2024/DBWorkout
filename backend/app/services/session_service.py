from app.db.models.session import Session
from app.db.models.course import Course
from app.db.session import SessionLocal
import logging

# Create a new session
def create_session(data, professor_id):
    session = SessionLocal()
    try:
        course_id = data.get("course_id")
        session_name = data.get("session_name")
        session_date = data.get("session_date")

        if not course_id or not session_name or not session_date:
            raise ValueError("course_id, session_name, and session_date are required")

        # Ensure professor owns the course
        course = session.query(Course).filter_by(course_id=course_id, professor_id=professor_id).first()
        if not course:
            raise ValueError("Unauthorized - You do not own this course")

        new_session = Session(course_id=course_id, session_name=session_name, session_date=session_date)
        session.add(new_session)
        session.commit()

        return {
            "session_id": new_session.session_id,
            "course_id": course_id,
            "session_name": session_name,
            "session_date": session_date
        }
    except Exception as e:
        session.rollback()
        logging.error(f"Error in create_session: {e}")
        raise e
    finally:
        session.close()

# Get sessions (Professors can see all, Students see enrolled)
def get_sessions(course_id, user_id, role):
    session = SessionLocal()
    try:
        if not course_id:
            raise ValueError("course_id is required")

        if role == "professor":
            sessions = session.query(Session).filter_by(course_id=course_id).all()
        else:  # Students should only see sessions in enrolled courses
            sessions = session.query(Session).filter_by(course_id=course_id).all()

        return [
            {
                "session_id": s.session_id,
                "course_id": s.course_id,
                "session_name": s.session_name,
                "session_date": s.session_date
            }
            for s in sessions
        ]
    finally:
        session.close()

# Update session
def update_session(session_id, data, professor_id):
    session = SessionLocal()
    try:
        existing_session = session.query(Session).get(session_id)
        if not existing_session:
            raise ValueError("Session not found")

        # Ensure professor owns the course
        if existing_session.course.professor_id != professor_id:
            raise ValueError("Unauthorized - You do not own this course")

        existing_session.session_name = data.get("session_name", existing_session.session_name)
        existing_session.session_date = data.get("session_date", existing_session.session_date)

        session.commit()
        return {
            "session_id": existing_session.session_id,
            "course_id": existing_session.course_id,
            "session_name": existing_session.session_name,
            "session_date": existing_session.session_date
        }
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Delete session
def delete_session(session_id, professor_id):
    session = SessionLocal()
    try:
        session_obj = session.query(Session).get(session_id)
        if not session_obj:
            raise ValueError("Session not found")

        if session_obj.course.professor_id != professor_id:
            raise ValueError("Unauthorized - You do not own this course")

        session.delete(session_obj)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_session_by_id(session_id):
    session = SessionLocal()
    try:
        session_obj = session.query(Session).get(session_id)
        if not session_obj:
            return None  # Avoid raising an error here
        return {
            "session_id": session_obj.session_id,
            "course_id": session_obj.course_id,
            "session_name": session_obj.session_name,
            "session_date": session_obj.session_date
        }
    finally:
        session.close()