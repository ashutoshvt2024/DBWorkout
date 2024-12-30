# app/db/models/submission.py
from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.task_id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    submitted_query = Column(Text, nullable=False)
    submission_time = Column(TIMESTAMP, nullable=False, server_default=func.now())
    is_correct = Column(Boolean)

    # Relationship to Task
    task = relationship("Task", back_populates="submissions")
    user = relationship("User")