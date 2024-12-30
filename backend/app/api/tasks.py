# from flask import Blueprint, jsonify
# from sqlalchemy.sql import text  # Import text
# from app.db.session import SandboxSessionLocal

# tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")

# @tasks_blueprint.route("/sandbox/populate", methods=["POST"])
# def populate_sandbox():
#     session = SandboxSessionLocal()
#     try:
#         # Drop existing tables to reset the sandbox
#         session.execute(text("DROP TABLE IF EXISTS employees"))
#         session.execute(text("DROP TABLE IF EXISTS departments"))

#         # Create mock tables
#         session.execute(text("""
#         CREATE TABLE employees (
#             emp_id SERIAL PRIMARY KEY,
#             name VARCHAR(100),
#             salary INT,
#             dept_id INT
#         )
#         """))
#         session.execute(text("""
#         CREATE TABLE departments (
#             dept_id SERIAL PRIMARY KEY,
#             dept_name VARCHAR(100)
#         )
#         """))

#         # Insert mock data
#         session.execute(text("INSERT INTO departments (dept_id, dept_name) VALUES (1, 'HR'), (2, 'Engineering')"))
#         session.execute(text("INSERT INTO employees (name, salary, dept_id) VALUES ('Alice', 50000, 1), ('Bob', 70000, 2), ('Charlie', 60000, 1)"))

#         session.commit()
#         return jsonify({"message": "Sandbox database populated successfully!"}), 200
#     except Exception as e:
#         session.rollback()
#         return jsonify({"error": str(e)}), 500
#     finally:
#         session.close()
from flask import Blueprint, jsonify, request
from sqlalchemy.sql import text
from app.db.session import SandboxSessionLocal
from app.utils.auth import is_instructor  # A utility to check user privileges

tasks_blueprint = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_blueprint.route("/sandbox/populate", methods=["POST"])
def custom_populate_sandbox():
    """
    Allows instructors to create custom tables and populate data.
    """
    session = SandboxSessionLocal()
    try:
        # # Validate instructor privileges
        # user = request.headers.get("user_id")  # Fetch user ID from headers (or session token)
        # if not is_instructor(user):  # Check if the user is an instructor
        #     return jsonify({"error": "Unauthorized access. Only instructors can perform this action."}), 403

        # Get table creation and insertion details from request body
        data = request.json
        if not data or "schema" not in data or "tables" not in data:
            return jsonify({"error": "Invalid request. 'schema' and 'tables' fields are required."}), 400

        # Execute schema creation (if applicable)
        schema_name = data.get("schema")
        if schema_name:
            session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))

        # Iterate through the tables and create them
        for table in data["tables"]:
            table_name = table.get("name")
            columns = table.get("columns")
            rows = table.get("rows")

            if not table_name or not columns:
                return jsonify({"error": f"Invalid table definition for table: {table_name}"}), 400

            # Create table
            column_definitions = ", ".join([f"{col['name']} {col['type']}" for col in columns])
            session.execute(text(f"CREATE TABLE {schema_name}.{table_name} ({column_definitions})"))

            # Insert data if rows are provided
            if rows:
                for row in rows:
                    columns_names = ", ".join([col["name"] for col in columns])
                    values_placeholders = ", ".join([f":{col['name']}" for col in columns])
                    session.execute(
                        text(f"INSERT INTO {schema_name}.{table_name} ({columns_names}) VALUES ({values_placeholders})"),
                        row
                    )

        session.commit()
        return jsonify({"message": "Custom tables and data populated successfully!"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()