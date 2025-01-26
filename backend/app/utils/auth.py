from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.db.models.user import User  # Assuming a User model exists
from app.db.session import SessionLocal

auth_blueprint = Blueprint("auth", __name__)

# Check if a user is an instructor
def is_instructor(user_id):
    """
    Check if a user is an instructor.
    :param user_id: ID of the user to check.
    :return: True if the user is an instructor, False if not, or None if the user doesn't exist.
    """
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None  # User not found
        return user.role == "instructor"
    except SQLAlchemyError as e:
        print(f"Database error: {e}")  # Debugging/logging
        return False
    finally:
        session.close()