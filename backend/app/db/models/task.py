from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.session import Base
from sqlalchemy import Boolean
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
    published = Column(Boolean, default=False)  # New column to track published status

    # Relationships
    course = relationship("Course", back_populates="tasks")
    session = relationship("Session", back_populates="tasks")
    schema = relationship("Schema", back_populates="tasks")
    assignments = relationship("Assignment", back_populates="task")

    def to_dict(self, hide_correct_answer=False):
        task_dict = {
            "task_id": self.task_id,
            "task_title": self.task_title,
            "task_description": self.task_description,
            "course_id": self.course_id,
            "session_id": self.session_id,
            "schema_id": self.schema_id,
            "difficulty": self.difficulty,
            "tags": self.tags,
            "deadline": str(self.deadline),
            "created_at": str(self.created_at),
            "published": self.published  # Include published status in the dictionary
        }
        if not hide_correct_answer:
            task_dict["correct_answer"] = self.correct_answer
        return task_dict