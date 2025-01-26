from flask import Blueprint, request, jsonify
from app.services.schema_service import (
    create_schema,
    list_schemas,
    get_schema_by_id,
    create_table_in_schema,
    alter_table_in_schema,
    delete_table_from_schema,
)

schemas_blueprint = Blueprint("schemas", __name__)

# Create a new schema
@schemas_blueprint.route("/schemas", methods=["POST"])
def create():
    data = request.json
    try:
        new_schema = create_schema(data)
        return jsonify({"message": "Schema created successfully", "schema": new_schema}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# List all schemas for a professor
@schemas_blueprint.route("/schemas", methods=["GET"])
def list_all():
    professor_id = request.args.get("professor_id")
    try:
        schemas = list_schemas(professor_id)
        return jsonify({"schemas": schemas}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get schema details by ID
@schemas_blueprint.route("/schemas/<int:schema_id>", methods=["GET"])
def get_details(schema_id):
    try:
        schema = get_schema_by_id(schema_id)
        return jsonify({"schema": schema}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# Create a table in a specific schema
@schemas_blueprint.route("/schemas/<int:schema_id>/tables", methods=["POST"])
def create_table(schema_id):
    data = request.json
    try:
        table = create_table_in_schema(schema_id, data)
        return jsonify({"message": "Table created successfully", "table": table}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Alter an existing table in the schema
@schemas_blueprint.route("/schemas/<int:schema_id>/tables/<string:table_name>", methods=["PUT"])
def alter_table(schema_id, table_name):
    data = request.json
    try:
        updated_table = alter_table_in_schema(schema_id, table_name, data)
        return jsonify({"message": "Table altered successfully", "table": updated_table}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a table from the schema
@schemas_blueprint.route("/schemas/<int:schema_id>/tables/<string:table_name>", methods=["DELETE"])
def delete_table(schema_id, table_name):
    try:
        delete_table_from_schema(schema_id, table_name)
        return jsonify({"message": "Table deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400