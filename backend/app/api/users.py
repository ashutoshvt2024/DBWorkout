from flask import Blueprint, jsonify, request
from app.db.session import SessionLocal
from app.db.models.user import User

user_blueprint = Blueprint("user", __name__, url_prefix="/users")

@user_blueprint.route("/", methods=["GET"])
def get_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return jsonify([{"id": user.user_id, "name": user.name, "email": user.email} for user in users])

@user_blueprint.route("/", methods=["POST"])
def create_user():
    session = SessionLocal()
    data = request.json
    new_user = User(name=data["name"], email=data["email"], role=data["role"])
    session.add(new_user)
    session.commit()
    session.close()
    return jsonify({"message": "User created successfully!"}), 201