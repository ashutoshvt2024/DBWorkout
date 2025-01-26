from datetime import datetime, timezone
from sqlalchemy import Column, Date, DateTime, Enum, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class TaskTimeTracking(Base):
    __tablename__ = "task_time_tracking"

    tracking_id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"), nullable=False)
    event_type = Column(Enum("start", "pause", "resume", "submit", name="time_event_types"), nullable=False)
    event_timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    assignment = relationship("Assignment", back_populates="time_tracking")