from datetime import datetime, timezone
from sqlalchemy import Column, Date, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String(255), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    session_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    course = relationship("Course", back_populates="sessions")
    tasks = relationship("Task", back_populates="session")