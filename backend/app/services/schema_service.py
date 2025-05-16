from app.db.models.schema import Schema
from app.db.session import SessionLocal
import logging
from sqlalchemy import Table, text
# Create a new schema
def create_schema(data):
    session = SessionLocal()
    try:
        schema_name = data.get("schema_name")
        professor_id = data.get("professor_id")

        if not schema_name or not professor_id:
            raise ValueError("schema_name and professor_id are required")

        # Create schema model in the database
        new_schema = Schema(schema_name=schema_name, created_by=professor_id)
        session.add(new_schema)

        # Dynamically create the schema using raw SQL
        create_schema_sql = text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
        session.execute(create_schema_sql)
        session.commit()

        return {"schema_id": new_schema.schema_id, "schema_name": schema_name, "created_by": professor_id}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# List all schemas created by a professor
def list_schemas(professor_id):
    session = SessionLocal()
    try:
        schemas = session.query(Schema).filter_by(created_by=professor_id).all()
        return [{"schema_id": schema.schema_id, "schema_name": schema.schema_name} for schema in schemas]
    finally:
        session.close()

# Get schema details by ID
def get_schema_by_id(schema_id):
    session = SessionLocal()
    try:
        schema = session.query(Schema).get(schema_id)
        if not schema:
            raise ValueError("Schema not found")

        # ✅ Fetch tables belonging to this schema
        tables = session.execute(
            text(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema.schema_name}'")
        ).fetchall()

        table_names = [table[0] for table in tables]  # Extract table names

        return {
            "schema_id": schema.schema_id,
            "schema_name": schema.schema_name,
            "tables": table_names,  # ✅ Return tables list
        }
    except Exception as e:
        logging.error(f"Error fetching schema: {str(e)}")
        return None
    finally:
        session.close()

# Create a table in a specific schema
def create_table_in_schema(schema_id, data):
    session = SessionLocal()
    try:
        schema = session.query(Schema).get(schema_id)
        if not schema:
            raise ValueError("Schema not found")

        table_name = data.get("table_name")
        columns = data.get("columns")  # List of column definitions
        if not table_name or not columns:
            raise ValueError("table_name and columns are required")

        # ✅ Ensure schema name is correctly formatted
        schema_name = schema.schema_name
        if " " in schema_name:  # If schema has spaces, wrap in double quotes
            schema_name = f'"{schema_name}"'

        # ✅ Ensure table name is also wrapped in double quotes if it contains spaces
        if " " in table_name:
            table_name = f'"{table_name}"'

        # ✅ Ensure schema exists before using it
        ensure_schema_sql = text(f'CREATE SCHEMA IF NOT EXISTS {schema_name}')
        session.execute(ensure_schema_sql)

        # ✅ Construct column definitions safely
        column_definitions = ", ".join([f"{col['name']} {col['type']}" for col in columns])

        # ✅ Create table inside the schema
        create_table_sql = text(f"CREATE TABLE {schema_name}.{table_name} ({column_definitions});")

        # Execute queries
        session.execute(create_table_sql)
        session.commit()

        return {"schema_id": schema_id, "table_name": table_name}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Alter an existing table in the schema
def alter_table_in_schema(schema_id, table_name, data):
    session = SessionLocal()
    try:
        schema = session.query(Schema).get(schema_id)
        if not schema:
            raise ValueError("Schema not found")

        schema_name = schema.schema_name
        sql_command = data.get("sql_command")  # 🔹 SQL command from SQL mode

        # 🔹 If SQL Mode is used, execute the given SQL command directly
        if sql_command:
            alter_table_query = text(sql_command)
        else:
            # 🔹 If UI Mode is used, construct the SQL ALTER statement dynamically
            column_updates = data.get("column_updates")  # [{"column_name": "age", "new_type": "VARCHAR(20)"}]
            if not column_updates:
                raise ValueError("column_updates or sql_command required")

            column_changes = ", ".join([f"ALTER COLUMN {col['column_name']} TYPE {col['new_type']}" for col in column_updates])
            alter_table_query = text(f"ALTER TABLE {schema_name}.{table_name} {column_changes};")

        session.execute(alter_table_query)
        session.commit()

        return {"message": "Table updated successfully", "schema_id": schema_id, "table_name": table_name}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Delete a table from the schema
def delete_table_from_schema(schema_id, table_name):
    session = SessionLocal()
    try:
        schema = session.query(Schema).get(schema_id)
        if not schema:
            raise ValueError("Schema not found")

        schema_name = schema.schema_name

        delete_table_sql = text(f"DROP TABLE IF EXISTS {schema_name}.{table_name};")

        session.execute(delete_table_sql)
        session.commit()

        return {"message": "Table deleted successfully", "schema_id": schema_id}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def execute_sql_on_schema(schema_id, sql_command):
    session = SessionLocal()
    try:
        schema = session.query(Schema).get(schema_id)
        if not schema:
            raise ValueError("Schema not found")

        schema_name = schema.schema_name

        # ✅ Ensure command is properly formatted
        safe_sql = text(sql_command.replace("SCHEMA_NAME", schema_name))

        session.execute(safe_sql)
        session.commit()

        return {"message": "SQL command executed successfully"}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def insert_into_table(schema_id, table_name, rows):
    session = SessionLocal()
    try:
        schema = session.query(Schema).get(schema_id)
        if not schema:
            raise ValueError("Schema not found")

        schema_name = schema.schema_name

        # Construct the INSERT query dynamically
        for row in rows:
            columns = ", ".join(row.keys())
            values = ", ".join([f":{key}" for key in row.keys()])
            insert_sql = text(f"INSERT INTO {schema_name}.{table_name} ({columns}) VALUES ({values});")
            session.execute(insert_sql, row)

        session.commit()
        return {"message": "Rows inserted successfully", "schema_id": schema_id, "table_name": table_name}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
# Fetch data from a table in a schema
def fetch_table_data(schema_id, table_name):
    session = SessionLocal()
    try:
        schema = session.query(Schema).get(schema_id)
        if not schema:
            raise ValueError("Schema not found")

        schema_name = schema.schema_name

        # Fetch all rows from the table
        fetch_sql = text(f"SELECT * FROM {schema_name}.{table_name};")
        result = session.execute(fetch_sql).fetchall()

        # Convert rows to a list of dictionaries
        rows = [dict(row) for row in result]

        return {"schema_id": schema_id, "table_name": table_name, "rows": rows}
    except Exception as e:
        raise e
    finally:
        session.close()