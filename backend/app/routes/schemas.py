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
    insert_into_table
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
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can execute SQL commands"}), 403

    if not sql_command:
        return jsonify({"error": "SQL command is required"}), 400

    try:
        result = execute_sql_on_schema(schema_id, sql_command)
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error executing SQL command: {str(e)}")
        return jsonify({"error": str(e)}), 400

# ---------------------- INSERT ROWS INTO TABLE (PROFESSORS ONLY) ----------------------
@schemas_blueprint.route("/schemas/<int:schema_id>/tables/<string:table_name>/rows", methods=["POST"])
@jwt_required()
def insert_rows(schema_id, table_name):
    data = request.json
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can insert rows"}), 403

    rows = data.get("rows")
    if not rows or not isinstance(rows, list):
        return jsonify({"error": "Invalid payload. 'rows' must be a list of dictionaries"}), 400

    try:
        result = insert_into_table(schema_id, table_name, rows)
        return jsonify(result), 201
    except Exception as e:
        logging.error(f"Error inserting rows into table: {str(e)}")
        return jsonify({"error": str(e)}), 400


# ---------------------- UPDATE ROW IN TABLE (PROFESSORS ONLY) ----------------------
@schemas_blueprint.route("/schemas/<int:schema_id>/tables/<string:table_name>/rows/<int:row_id>", methods=["PUT"])
@jwt_required()
def update_row(schema_id, table_name, row_id):
    data = request.json
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can update rows"}), 403

    updates = data.get("updates")
    if not updates or not isinstance(updates, dict):
        return jsonify({"error": "Invalid payload. 'updates' must be a dictionary"}), 400

    try:
        set_clause = ", ".join([f"{key} = '{value}'" for key, value in updates.items()])
        sql_command = f"UPDATE {table_name} SET {set_clause} WHERE id = {row_id};"
        result = execute_sql_on_schema(schema_id, sql_command)
        return jsonify({"message": "Row updated successfully", "result": result}), 200
    except Exception as e:
        logging.error(f"Error updating row: {str(e)}")
        return jsonify({"error": str(e)}), 400

# ---------------------- DELETE ROW FROM TABLE (PROFESSORS ONLY) ----------------------
@schemas_blueprint.route("/schemas/<int:schema_id>/tables/<string:table_name>/rows/<int:row_id>", methods=["DELETE"])
@jwt_required()
def delete_row(schema_id, table_name, row_id):
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can delete rows"}), 403

    try:
        sql_command = f"DELETE FROM {table_name} WHERE id = {row_id};"
        result = execute_sql_on_schema(schema_id, sql_command)
        return jsonify({"message": "Row deleted successfully", "result": result}), 200
    except Exception as e:
        logging.error(f"Error deleting row: {str(e)}")
        return jsonify({"error": str(e)}), 400

@schemas_blueprint.route("/schemas/<int:schema_id>/tables", methods=["GET"])
@jwt_required()
def fetch_tables(schema_id):
    try:
        schema = get_schema_by_id(schema_id)
        if not schema:
            return jsonify({"error": "Schema not found"}), 404

        tables = schema.get("tables", [])
        return jsonify({"schema_id": schema_id, "tables": tables}), 200
    except Exception as e:
        logging.error(f"Error fetching tables for schema {schema_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@schemas_blueprint.route("/schemas/<int:schema_id>/tables/<string:table_name>/columns", methods=["POST"])
@jwt_required()
def add_column(schema_id, table_name):
    data = request.json
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can add columns"}), 403

    column_name = data.get("column_name")
    column_type = data.get("column_type")

    if not column_name or not column_type:
        return jsonify({"error": "Both column_name and column_type are required"}), 400

    try:
        sql_command = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"
        result = execute_sql_on_schema(schema_id, sql_command)
        return jsonify({"message": "Column added successfully", "result": result}), 200
    except Exception as e:
        logging.error(f"Error adding column: {str(e)}")
        return jsonify({"error": str(e)}), 400

@schemas_blueprint.route("/schemas/<int:schema_id>/tables/<string:table_name>/columns/<string:column_name>", methods=["DELETE"])
@jwt_required()
def delete_column(schema_id, table_name, column_name):
    current_user = get_current_user()

    if current_user["role"] != "professor":
        return jsonify({"error": "Unauthorized - Only professors can delete columns"}), 403

    try:
        sql_command = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
        result = execute_sql_on_schema(schema_id, sql_command)
        return jsonify({"message": "Column deleted successfully", "result": result}), 200
    except Exception as e:
        logging.error(f"Error deleting column: {str(e)}")
        return jsonify({"error": str(e)}), 400