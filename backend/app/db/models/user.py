from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    course_instance_id = Column(Integer, ForeignKey("course_instances.course_instance_id"))

    # Use string reference to resolve circular dependency
    course_instance = relationship("CourseInstance", back_populates="users")