from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError
from app.core.config import Config
import logging

# Database engine
engine = create_engine(Config.DATABASE_URL)

# Execute a SQL query in a specific schema
def execute_query(schema_name, query):
    """
    Execute a SQL query in the specified schema.
    :param schema_name: Name of the schema where the query should be executed.
    :param query: The SQL query to execute.
    :return: Query results as a list of dictionaries or an error message.
    """
    try:
        with engine.connect() as connection:
            # Switch to the specific schema
            connection.execute(text("SET search_path TO :schema_name"), {"schema_name": schema_name})
            # Execute the query
            result = connection.execute(text(query))
            # Fetch all rows and return as a list of dictionaries
            return [dict(row) for row in result.fetchall()]
    except ProgrammingError as pe:
        logging.error(f"Query failed: {pe}")
        return {"error": f"Query failed: {str(pe)}"}
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        return {"error": f"Database error: {str(e)}"}

# Validate a student's query against the correct answer
def validate_query(submitted_query, correct_answer, schema_name):
    """
    Compare the results of the submitted query with the correct answer.
    :param submitted_query: The SQL query submitted by the student.
    :param correct_answer: The correct SQL query.
    :param schema_name: Name of the schema where the queries will be executed.
    :return: A dictionary with validation status and feedback.
    """
    try:
        # Execute both queries
        submitted_result = execute_query(schema_name, submitted_query)
        correct_result = execute_query(schema_name, correct_answer)

        # Check for execution errors
        if "error" in submitted_result:
            return {
                "is_correct": False,
                "feedback": generate_feedback(submitted_result["error"]),
            }
        if "error" in correct_result:
            return {
                "is_correct": False,
                "feedback": generate_feedback(correct_result["error"]),
            }

        # Compare results
        if submitted_result == correct_result:
            return {"is_correct": True, "feedback": "Your query is correct!"}
        else:
            differences = f"Expected: {correct_result}, Got: {submitted_result}"
            return {
                "is_correct": False,
                "feedback": f"The results do not match. {differences}",
            }
    except Exception as e:
        logging.error(f"Validation error: {e}")
        return {"is_correct": False, "feedback": "An internal error occurred during validation."}

# Generate feedback if the query fails
def generate_feedback(error):
    """
    Generate user-friendly feedback based on the error message.
    :param error: The error message from query execution.
    :return: Feedback message.
    """
    if "syntax error" in error.lower():
        return "There seems to be a syntax error in your query. Please check the SQL syntax."
    elif "relation" in error.lower() and "does not exist" in error.lower():
        return "It seems you are trying to query a table that does not exist in the schema."
    elif "column" in error.lower() and "does not exist" in error.lower():
        return "One or more columns in your query do not exist. Please check your column names."
    elif "permission denied" in error.lower():
        return "You do not have the necessary permissions to execute this query."
    else:
        return f"An error occurred while executing your query: {error}"