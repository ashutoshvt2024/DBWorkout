from sqlalchemy.orm import Session
import json
from sqlalchemy.sql import text

def canonicalize_results(results):
    """
    Sort and convert query results to a canonical form for comparison.
    """
    return sorted([tuple(row) for row in results])

def execute_and_compare(user_query, solution_query, sandbox_session: Session):
    try:
        # Execute the queries
        expected_result = sandbox_session.execute(text(solution_query)).fetchall()
        user_result = sandbox_session.execute(text(user_query)).fetchall()

        # Canonicalize results
        expected_result_canonical = canonicalize_results(expected_result)
        user_result_canonical = canonicalize_results(user_result)

        # Compare canonicalized results
        is_correct = (expected_result_canonical == user_result_canonical)

        return {
            "is_correct": is_correct,
            "expected_result": expected_result_canonical,
            "user_result": user_result_canonical
        }
    except Exception as e:
        return {
            "is_correct": False,
            "error": str(e)
        }