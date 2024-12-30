from app.db.models.user import User  # Assuming a User model exists
from app.db.session import  SessionLocal
def is_instructor(user_id):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        return user and user.role == "instructor"  # Check if the user's role is 'instructor'
    except:
        return False
    finally:
        session.close()