from flask import Blueprint, request, jsonify, make_response
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from app.db.session import SessionLocal
from app.db.models.user import User
import logging
import json

auth_blueprint = Blueprint("auth", __name__)
CORS(auth_blueprint, resources={r"/*": {"origins": "http://localhost:3000"}})  # ✅ Apply CORS
logging.basicConfig(level=logging.INFO)

# ---------------------- REGISTER USER ----------------------
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
        # Check if user exists
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            logging.warning(f"Registration failed: Email {email} already exists.")
            return jsonify({"error": "Email already exists"}), 409

        # Hash the password and create the user
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

# ---------------------- LOGIN USER ----------------------
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
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        # ✅ Fix: Directly store user_id and role at top level (not inside `sub`)
        access_token = create_access_token(identity=json.dumps({"user_id": user.user_id, "role": user.role}))

        return jsonify({"message": "Login successful", "access_token": access_token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()
# ---------------------- GET USER INFO ----------------------
@auth_blueprint.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    identity = get_jwt_identity()
    return jsonify(identity), 200

# ---------------------- LOGOUT ----------------------
@auth_blueprint.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    unset_jwt_cookies(response)  # Remove JWT tokens from cookies
    return response, 200

# ---------------------- REFRESH TOKEN ----------------------
@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    response = make_response(jsonify({"message": "Token refreshed"}))
    set_access_cookies(response, new_access_token)
    return response, 200