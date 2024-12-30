from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.session_id", ondelete="CASCADE"))
    question_text = Column(Text, nullable=False)
    solution_query = Column(Text, nullable=False)
    category = Column(String(50))

    # Relationship to Submissions
    submissions = relationship("Submission", back_populates="task")

    # Relationship to Session
    session = relationship("Session", back_populates="tasks")