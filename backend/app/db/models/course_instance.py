from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class CourseInstance(Base):
    __tablename__ = "course_instances"

    course_instance_id = Column(Integer, primary_key=True,index=True)
    course_name = Column(String(100), nullable=False)
    semester = Column(String(20), nullable=False)

    # Back-reference to users
    users = relationship("User", back_populates="course_instance")