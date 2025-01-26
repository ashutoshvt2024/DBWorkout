from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("professor", "student", name="user_roles"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    courses = relationship("Course", back_populates="professor")
    schemas = relationship("Schema", back_populates="creator")
    assignments = relationship("Assignment", back_populates="student")
    enrollments = relationship("Enrollment", back_populates="student")  # Use string reference