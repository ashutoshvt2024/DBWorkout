# app/db/models/submission.py
from sqlalchemy import Column, DateTime, Integer, Text, Boolean, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime, timezone

class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"), nullable=False)
    submitted_query = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    submitted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    assignment = relationship("Assignment", back_populates="submissions")