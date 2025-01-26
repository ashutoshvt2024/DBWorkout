from flask import Blueprint, request, jsonify
from app.services.user_service import get_user_by_id, update_user, delete_user
import logging

user_blueprint = Blueprint("user", __name__)
logging.basicConfig(level=logging.INFO)

# Fetch a specific user by ID
@user_blueprint.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = get_user_by_id(user_id)
        return jsonify({"user": user}), 200
    except ValueError as ve:
        logging.warning(f"User fetch failed: {ve}")
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        logging.error(f"Unexpected error in get_user: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


# Update user details
@user_blueprint.route("/users/<int:user_id>", methods=["PUT"])
def update(user_id):
    data = request.json
    try:
        updated_user = update_user(user_id, data)
        return jsonify({"message": "User updated successfully", "user": updated_user}), 200
    except ValueError as ve:
        logging.warning(f"User update failed: {ve}")
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        logging.error(f"Unexpected error in update: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


# Delete a user
@user_blueprint.route("/users/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    try:
        delete_user(user_id)
        return jsonify({"message": "User deleted successfully"}), 200
    except ValueError as ve:
        logging.warning(f"User deletion failed: {ve}")
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        logging.error(f"Unexpected error in delete: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500