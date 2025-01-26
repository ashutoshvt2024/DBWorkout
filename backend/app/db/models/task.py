from datetime import datetime, timezone
from sqlalchemy import Column, Date, DateTime, Enum, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    task_title = Column(String(255), nullable=False)
    task_description = Column(Text, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.session_id"), nullable=False)
    schema_id = Column(Integer, ForeignKey("schemas.schema_id"), nullable=False)
    correct_answer = Column(Text, nullable=False)
    difficulty = Column(Enum("easy", "medium", "hard", name="task_difficulty"), default="medium", nullable=False)
    tags = Column(String(255), nullable=True)
    deadline = Column(Date, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    course = relationship("Course", back_populates="tasks")
    session = relationship("Session", back_populates="tasks")
    schema = relationship("Schema", back_populates="tasks")
    assignments = relationship("Assignment", back_populates="task")