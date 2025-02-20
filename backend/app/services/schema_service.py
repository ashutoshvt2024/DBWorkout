from app.db.models.schema import Schema
from app.db.session import SessionLocal
from sqlalchemy import text
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
        return {"schema_id": schema.schema_id, "schema_name": schema.schema_name}
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

        alter_sql = data.get("alter_sql")  # Direct SQL for altering
        if not alter_sql:
            raise ValueError("alter_sql is required")

        schema_name = schema.schema_name

        # ✅ Ensure schema and table names are properly wrapped if they contain spaces
        if " " in schema_name:
            schema_name = f'"{schema_name}"'
        if " " in table_name:
            table_name = f'"{table_name}"'

        # ✅ Wrap the SQL command in `text()` to avoid the SQLAlchemy error
        alter_table_query = text(f"ALTER TABLE {schema_name}.{table_name} {alter_sql};")
        session.execute(alter_table_query)
        session.commit()

        return {"schema_id": schema_id, "table_name": table_name}
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

        # ✅ Ensure schema name is properly formatted
        if " " in schema_name:
            schema_name = f'"{schema_name}"'

        # ✅ Ensure table name is properly formatted
        if " " in table_name:
            table_name = f'"{table_name}"'

        # ✅ Fix: Use text() for the SQL query
        delete_table_sql = text(f"DROP TABLE IF EXISTS {schema_name}.{table_name};")

        # Execute query
        session.execute(delete_table_sql)
        session.commit()

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()