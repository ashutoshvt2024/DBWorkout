from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.schema_service import (
    create_schema,
    execute_sql_on_schema,
    list_schemas,
    get_schema_by_id,
    create_table_in_schema,
    alter_table_in_schema,
    delete_table_from_schema,
)
from sqlalchemy import text
import json
import logging

schemas_blueprint = Blueprint("schemas", __name__)
logging.basicConfig(level=logging.INFO)

# ✅ Utility function for extracting JWT user
def get_current_user():
    identity = get_jwt_identity()
    try:
        identity = json.loads(identity)
    except json.JSONDecodeError:
        pass
    return identity

# ---------------------- CREATE SCHEMA (PROFESSORS ONLY) ----------------------
@schemas_blueprint.route("/schemas", methods=["POST"])
@jwt_required()
def create_schema_route():
    data = request.json
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can create schemas"}), 403

    data["professor_id"] = current_user["user_id"]  # Ensure professor_id is correctly assigned
    try:
        new_schema = create_schema(data)
        return jsonify({"message": "Schema created successfully", "schema": new_schema}), 201
    except Exception as e:
        logging.error(f"Error creating schema: {str(e)}")
        return jsonify({"error": str(e)}), 400

# ---------------------- LIST SCHEMAS (PROFESSORS & STUDENTS) ----------------------
@schemas_blueprint.route("/schemas", methods=["GET"])
@jwt_required()
def list_schemas_route():
    current_user = get_current_user()

    try:
        schemas = list_schemas(professor_id=current_user["user_id"]) if current_user["role"] == "professor" else []
        return jsonify({"schemas": schemas}), 200
    except Exception as e:
        logging.error(f"Error listing schemas: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ---------------------- GET SCHEMA DETAILS (PROFESSORS & STUDENTS) ----------------------
@schemas_blueprint.route("/schemas/<int:schema_id>", methods=["GET"])
@jwt_required()
def get_schema_details(schema_id):
    try:
        schema = get_schema_by_id(schema_id)
        if not schema:
            return jsonify({"error": "Schema not found"}), 404
        return jsonify(schema), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------- CREATE TABLE IN SCHEMA (PROFESSORS ONLY) ----------------------
@schemas_blueprint.route("/schemas/<int:schema_id>/tables", methods=["POST"])
@jwt_required()
def create_table_route(schema_id):
    data = request.json
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can create tables"}), 403

    try:
        table = create_table_in_schema(schema_id, data)
        return jsonify({"message": "Table created successfully", "table": table}), 201
    except Exception as e:
        logging.error(f"Error creating table: {str(e)}")
        return jsonify({"error": str(e)}), 400

# ---------------------- ALTER TABLE IN SCHEMA (PROFESSORS ONLY) ----------------------
@schemas_blueprint.route("/schemas/<int:schema_id>/tables/<string:table_name>", methods=["PUT"])
@jwt_required()
def alter_table(schema_id, table_name):
    data = request.json
    try:
        result = alter_table_in_schema(schema_id, table_name, data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------------------- DELETE TABLE FROM SCHEMA (PROFESSORS ONLY) ----------------------
@schemas_blueprint.route("/schemas/<int:schema_id>/tables/<string:table_name>", methods=["DELETE"])
@jwt_required()
def delete_table(schema_id, table_name):
    try:
        result = delete_table_from_schema(schema_id, table_name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 🔹 Execute SQL Query on Schema
@schemas_blueprint.route("/schemas/<int:schema_id>/execute", methods=["POST"])
@jwt_required()
def execute_sql(schema_id):
    data = request.json
    sql_command = data.get("sql_command")
    try:
        result = execute_sql_on_schema(schema_id, sql_command)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400