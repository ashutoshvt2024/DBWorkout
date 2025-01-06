from flask import Blueprint, jsonify, request
from sqlalchemy.sql import text
from app.db.session import SandboxSessionLocal

schemas_blueprint = Blueprint("schemas", __name__, url_prefix="/schemas")


@schemas_blueprint.route("/", methods=["GET"])
def get_schemas():
    """
    Fetch all schemas from the database.
    """
    session = SandboxSessionLocal()
    try:
        result = session.execute(
            text("SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast');")
        )
        # Access rows as tuples and extract schema_name
        schemas = [row[0] for row in result]  # Use row[0] because it's a single-column query
        return jsonify({"schemas": schemas}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@schemas_blueprint.route("/", methods=["POST"])
def create_schema():
    """
    Create a new schema in the database.
    """
    session = SandboxSessionLocal()
    try:
        data = request.json
        schema_name = data.get("schema_name")

        if not schema_name:
            return jsonify({"error": "Schema name is required."}), 400

        # Create schema
        session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
        session.commit()
        return jsonify({"message": "Schema created successfully!"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@schemas_blueprint.route("/<schema_name>", methods=["DELETE"])
def delete_schema(schema_name):
    """
    Delete a schema from the database.
    """
    session = SandboxSessionLocal()
    try:
        if not schema_name:
            return jsonify({"error": "Schema name is required."}), 400

        # Drop schema
        session.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE"))
        session.commit()
        return jsonify({"message": "Schema deleted successfully!"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@schemas_blueprint.route("/<schema_name>/tables", methods=["GET"])
def get_tables(schema_name):
    """
    Fetch all tables in the specified schema.
    """
    session = SandboxSessionLocal()
    try:
        result = session.execute(
            text(f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = :schema_name
            """),
            {"schema_name": schema_name}
        )
        tables = [row[0] for row in result]
        return jsonify({"tables": tables}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@schemas_blueprint.route("/<schema_name>/tables", methods=["POST"])
def create_table(schema_name):
    """
    Create a new table in the specified schema.
    """
    session = SandboxSessionLocal()
    try:
        data = request.json
        table_name = data.get("table_name")
        columns = data.get("columns", [])

        if not table_name or not columns:
            return jsonify({"error": "Table name and columns are required."}), 400

        column_definitions = ", ".join([f"{col['name']} {col['type']}" for col in columns])
        session.execute(text(f"CREATE TABLE {schema_name}.{table_name} ({column_definitions})"))
        session.commit()
        return jsonify({"message": "Table created successfully!"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@schemas_blueprint.route("/<schema_name>/tables/<table_name>/rows", methods=["POST"])
def insert_rows(schema_name, table_name):
    """
    Insert rows into the specified table.
    """
    session = SandboxSessionLocal()
    try:
        data = request.json
        rows = data.get("rows", [])

        if not rows:
            return jsonify({"error": "Rows are required."}), 400

        for row in rows:
            columns = ", ".join(row.keys())
            placeholders = ", ".join([f":{key}" for key in row.keys()])
            session.execute(
                text(f"INSERT INTO {schema_name}.{table_name} ({columns}) VALUES ({placeholders})"),
                row
            )
        session.commit()
        return jsonify({"message": "Rows inserted successfully!"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@schemas_blueprint.route("/<schema_name>/tables/<table_name>", methods=["DELETE"])
def delete_table(schema_name, table_name):
    """
    Delete a table from the specified schema.
    """
    session = SandboxSessionLocal()
    try:
        session.execute(text(f"DROP TABLE {schema_name}.{table_name} CASCADE"))
        session.commit()
        return jsonify({"message": "Table deleted successfully!"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@schemas_blueprint.route("/<schema_name>/tables/<table_name>/rows", methods=["GET"])
def get_rows(schema_name, table_name):
    """
    Fetch rows from the specified table.
    """
    session = SandboxSessionLocal()
    try:
        # Execute query to fetch all rows
        result = session.execute(text(f"SELECT * FROM {schema_name}.{table_name}"))
        
        # Convert each row to a dictionary using `row._asdict()`
        rows = [dict(row._mapping) for row in result]
        
        return jsonify({"rows": rows}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@schemas_blueprint.route("/<schema_name>/tables/<table_name>/rows", methods=["DELETE"])
def delete_row(schema_name, table_name):
    """
    Delete rows in the specified table based on conditions.
    """
    session = SandboxSessionLocal()
    try:
        data = request.json
        conditions = data.get("conditions", {})

        # Validate that 'id' exists and is an integer
        row_id = conditions.get("id")
        if not isinstance(row_id, int):
            return jsonify({"error": "Valid 'id' is required for deletion."}), 400

        session.execute(
            text(f"DELETE FROM {schema_name}.{table_name} WHERE id = :id"),
            {"id": row_id}
        )
        session.commit()
        return jsonify({"message": "Row deleted successfully!"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@schemas_blueprint.route("/<schema_name>/tables/<table_name>/rows", methods=["PUT"])
def update_row(schema_name, table_name):
    """
    Update rows in the specified table based on conditions.
    """
    session = SandboxSessionLocal()
    try:
        data = request.json
        updates = data.get("updates", {})
        conditions = data.get("conditions", {})

        if not updates or "id" not in conditions:
            return jsonify({"error": "Updates and 'id' are required for updating rows."}), 400

        set_clause = ", ".join([f"{col} = :{col}" for col in updates.keys()])
        where_clause = f"id = :id"

        query_params = {**updates, **conditions}

        session.execute(
            text(f"UPDATE {schema_name}.{table_name} SET {set_clause} WHERE {where_clause}"),
            query_params
        )
        session.commit()
        return jsonify({"message": "Row updated successfully!"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()