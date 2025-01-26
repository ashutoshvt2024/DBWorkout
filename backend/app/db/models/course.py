from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.session import Base

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(255), nullable=False)
    professor_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    professor = relationship("User", back_populates="courses")
    sessions = relationship("Session", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")  # Use string reference
    tasks = relationship("Task", back_populates="course")