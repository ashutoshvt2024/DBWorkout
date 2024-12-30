from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    course_instance_id = Column(Integer, ForeignKey("course_instances.course_instance_id"), nullable=False)
    session_name = Column(String(100), nullable=False)
    schema_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    # Define relationship with tasks
    tasks = relationship("Task", back_populates="session")