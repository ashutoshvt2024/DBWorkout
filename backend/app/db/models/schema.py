from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Schema(Base):
    __tablename__ = "schemas"

    schema_id = Column(Integer, primary_key=True, index=True)
    schema_name = Column(String(255), nullable=False)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    creator = relationship("User", back_populates="schemas")
    tasks = relationship("Task", back_populates="schema")