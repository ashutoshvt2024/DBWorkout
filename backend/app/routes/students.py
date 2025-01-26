# from flask import Blueprint, jsonify
# from sqlalchemy import text
# from app.db.session import SessionLocal

# students_blueprint = Blueprint("students", __name__, url_prefix="/students")

# @students_blueprint.route("/<int:user_id>/progress", methods=["GET"])
# def fetch_student_progress(user_id):
#     """
#     Fetch individual student progress.
#     """
#     session = SessionLocal()
#     try:
#         query = """
#             SELECT 
#                 u.user_id AS user_id,
#                 u.name AS name,
#                 u.email AS email,
#                 COALESCE(SUM(l.task_completed_count), 0) AS tasks_completed,
#                 COALESCE(SUM(l.completion_time), 0) AS total_time_spent,
#                 CASE 
#                     WHEN SUM(l.task_completed_count) > 0 
#                     THEN SUM(l.completion_time) / SUM(l.task_completed_count)
#                     ELSE 0 
#                 END AS avg_time_per_task
#             FROM 
#                 users u
#             LEFT JOIN 
#                 leaderboard l ON u.user_id = l.user_id
#             WHERE 
#                 u.user_id = :user_id
#             GROUP BY 
#                 u.user_id, u.name, u.email;
#         """
#         result = session.execute(text(query), {"user_id": user_id}).mappings().first()

#         if not result:
#             return jsonify({"error": "Student not found"}), 404

#         return jsonify({
#             "user_id": result["user_id"],
#             "name": result["name"],
#             "email": result["email"],
#             "tasks_completed": result["tasks_completed"],
#             "total_time_spent": result["total_time_spent"],
#             "avg_time_per_task": result["avg_time_per_task"],
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         session.close()