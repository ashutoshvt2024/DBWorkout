from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.db.session import SessionLocal
from app.db.models.user import User
import logging
import json

auth_blueprint = Blueprint("auth", __name__)
logging.basicConfig(level=logging.INFO)

# Register a new user
@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")  # 'professor' or 'student'

    if not all([name, email, password, role]):
        return jsonify({"error": "All fields are required"}), 400

    session = SessionLocal()
    try:
        # Check if the email already exists
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            logging.warning(f"Registration failed: Email {email} already exists.")
            return jsonify({"error": "Email already exists"}), 409

        # Hash the password and save the new user
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password_hash=hashed_password, role=role)
        session.add(new_user)
        session.commit()

        logging.info(f"User registered: {email} with role {role}.")
        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        logging.error(f"Error during registration: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


# Login a user
@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    session = SessionLocal()
    try:
        user = session.query(User).filter_by(email=email).first()

        # Validate user and password
        if not user:
            logging.warning(f"Login failed: Email {email} not found.")
            return jsonify({"error": "Invalid email or password"}), 401

        if not check_password_hash(user.password_hash, password):
            logging.warning(f"Login failed: Incorrect password for email {email}.")
            return jsonify({"error": "Invalid email or password"}), 401

        # Serialize identity as a string
        access_token = create_access_token(identity={"user_id": user.user_id, "role": user.role})

        logging.info(f"User logged in: {email} with role {user.role}.")
        return jsonify({"message": "Login successful", "access_token": access_token}), 200

    except Exception as e:
        logging.error(f"Error during login: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()