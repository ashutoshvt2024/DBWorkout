from app.db.models.session import Session
from app.db.session import SessionLocal
import datetime
from flask import request, jsonify
# Create a new session in a course
def create_session(data):
    session = SessionLocal()
    try:
        course_id = data.get("course_id")
        session_name = data.get("session_name")
        session_date = data.get("session_date")

        if not course_id or not session_name or not session_date:
            raise ValueError("course_id, session_name, and session_date are required")

        new_session = Session(course_id=course_id, session_name=session_name, session_date=session_date)
        session.add(new_session)
        session.commit()

        return {"session_id": new_session.session_id, "course_id": course_id, "session_name": session_name, "session_date": session_date}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# List all sessions for a specific course
def get_sessions(course_id):
    session = SessionLocal()
    try:
        if not course_id:
            raise ValueError("course_id is required")

        sessions = session.query(Session).filter_by(course_id=course_id).all()
        return [{"session_id": s.session_id, "course_id": s.course_id, "session_name": s.session_name, "session_date": s.session_date} for s in sessions]
    finally:
        session.close()

# Fetch session details
def get_session_by_id(session_id):
    session = SessionLocal()
    try:
        session_obj = session.query(Session).get(session_id)
        if not session_obj:
            raise ValueError("Session not found")

        return {"session_id": session_obj.session_id, "course_id": session_obj.course_id, "session_name": session_obj.session_name, "session_date": session_obj.session_date}
    finally:
        session.close()

# Update session details
def update_session(session_id):
    data = request.json
    session = SessionLocal()
    try:
        # Retrieve the session to update
        existing_session = session.query(Session).get(session_id)
        if not existing_session:
            return jsonify({"error": "Session not found"}), 404

        # Update fields, ensuring course_id is preserved if not provided
        existing_session.session_name = data.get("session_name", existing_session.session_name)
        existing_session.session_date = data.get("session_date", existing_session.session_date)
        existing_session.course_id = data.get("course_id", existing_session.course_id)

        session.commit()
        return jsonify({"message": "Session updated successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# Delete a session
def delete_session(session_id):
    session = SessionLocal()
    try:
        session_obj = session.query(Session).get(session_id)
        if not session_obj:
            raise ValueError("Session not found")

        session.delete(session_obj)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()