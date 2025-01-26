from datetime import datetime, timezone
from sqlalchemy import Column, Date, DateTime, Enum, Float, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.task_id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    started_at = Column(DateTime, nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    status = Column(Enum("pending", "submitted", "graded", name="assignment_status"), default="pending")
    grade = Column(Float, nullable=True)
    submission_url = Column(String(255), nullable=True)
    assigned_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    task = relationship("Task", back_populates="assignments")
    student = relationship("User", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment")
    time_tracking = relationship("TaskTimeTracking", back_populates="assignment")