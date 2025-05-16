from app.db.models.course import Course
from app.db.session import SessionLocal
from app.db.models.assignment import Assignment
from app.db.models.enrollment import Enrollment
from app.db.models.user import User
import logging
# Create a new course
def create_course(data):
    session = SessionLocal()
    try:
        course_name = data.get("course_name")
        professor_id = data.get("professor_id")

        if not course_name or not isinstance(course_name, str):  # Ensure course_name is a string
            raise ValueError("course_name must be a non-empty string")
        if not professor_id or not isinstance(professor_id, int):  # Ensure professor_id is valid
            raise ValueError("professor_id must be an integer")

        new_course = Course(course_name=course_name, professor_id=professor_id)
        session.add(new_course)
        session.commit()
        return {
            "course_id": new_course.course_id,
            "course_name": new_course.course_name,
            "professor_id": new_course.professor_id,
        }
    except Exception as e:
        session.rollback()
        logging.error(f"Error in create_course: {e}")
        raise e
    finally:
        session.close()

# Get all courses
def get_courses(professor_id=None, student_id=None):
    session = SessionLocal()
    try:
        query = session.query(Course)
        if professor_id:
            query = query.filter(Course.professor_id == professor_id)
        if student_id:
            query = query.join(Course.enrollments).filter(Enrollment.student_id == student_id)
        courses = query.all()
        logging.info(f"Fetched courses: {courses}")
        return [
            {"course_id": course.course_id, "course_name": course.course_name, "professor_id": course.professor_id}
            for course in courses
        ]
    except Exception as e:
        logging.error(f"Error in get_courses: {e}")
        raise e
    finally:
        session.close()

# Get a course by ID
def get_course_by_id(course_id):
    session = SessionLocal()
    try:
        course = session.query(Course).get(course_id)
        if not course:
            raise ValueError("Course not found")
        return {"course_id": course.course_id, "course_name": course.course_name, "professor_id": course.professor_id}
    finally:
        session.close()

# Update a course
def update_course(course_id, data):
    session = SessionLocal()
    try:
        logging.info(f"Attempting to update course with ID: {course_id}")
        course = session.query(Course).filter_by(course_id=int(course_id)).first()  # Explicitly cast to int
        if not course:
            logging.error(f"Course with ID {course_id} not found")
            raise ValueError("Course not found")

        course.course_name = data.get("course_name", course.course_name)
        session.commit()
        logging.info(f"Course with ID {course_id} updated successfully")
        return {"course_id": course.course_id, "course_name": course.course_name, "professor_id": course.professor_id}
    except Exception as e:
        session.rollback()
        logging.error(f"Error updating course: {e}")
        raise e
    finally:
        session.close()

# Delete a course
def delete_course(course_id):
    session = SessionLocal()
    try:
        logging.info(f"Attempting to delete course with ID: {course_id}")
        course = session.query(Course).filter_by(course_id=int(course_id)).first()  # Explicitly cast to int
        if not course:
            logging.error(f"Course with ID {course_id} not found")
            raise ValueError("Course not found")

        session.delete(course)
        session.commit()
        logging.info(f"Course with ID {course_id} deleted successfully")
        return True
    except Exception as e:
        session.rollback()
        logging.error("Error deleting course: {e}")
        raise e
    finally:
        session.close()

def get_enrolled_courses(student_id):
    session = SessionLocal()
    try:
        # Query all courses the student is enrolled in
        enrolled_courses = session.query(Course).join(Course.enrollments).filter_by(student_id=student_id).all()
        return [{"course_id": course.course_id, "course_name": course.course_name} for course in enrolled_courses]
    finally:
        session.close()