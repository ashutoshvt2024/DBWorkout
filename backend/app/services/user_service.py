from app.db.models.user import User
from app.db.session import SessionLocal
from werkzeug.security import generate_password_hash
import logging

logging.basicConfig(level=logging.INFO)

# Get user by ID
def get_user_by_id(user_id):
    session = SessionLocal()
    try:
        user = session.query(User).get(user_id)
        if not user:
            raise ValueError("User not found")
        logging.info(f"User fetched: {user_id}")
        return {"user_id": user.user_id, "name": user.name, "email": user.email, "role": user.role}
    except Exception as e:
        logging.error(f"Error in get_user_by_id: {e}")
        raise e
    finally:
        session.close()


# Update user details
def update_user(user_id, data):
    session = SessionLocal()
    try:
        user = session.query(User).get(user_id)
        if not user:
            raise ValueError("User not found")

        user.name = data.get("name", user.name)
        user.email = data.get("email", user.email)
        if "password" in data:
            user.password_hash = generate_password_hash(data["password"])
        user.role = data.get("role", user.role)

        session.commit()
        logging.info(f"User updated: {user_id}")
        return {"user_id": user.user_id, "name": user.name, "email": user.email, "role": user.role}
    except Exception as e:
        session.rollback()
        logging.error(f"Error in update_user: {e}")
        raise e
    finally:
        session.close()


# Delete a user
def delete_user(user_id):
    session = SessionLocal()
    try:
        user = session.query(User).get(user_id)
        if not user:
            raise ValueError("User not found")

        session.delete(user)
        session.commit()
        logging.info(f"User deleted: {user_id}")
    except Exception as e:
        session.rollback()
        logging.error(f"Error in delete_user: {e}")
        raise e
    finally:
        session.close()