# app/db/models/leaderboard.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from app.db.session import Base

class Leaderboard(Base):
    __tablename__ = "leaderboard"

    leaderboard_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    course_instance_id = Column(Integer, ForeignKey("course_instances.course_instance_id", ondelete="CASCADE"))
    task_completed_count = Column(Integer, default=0)
    completion_time = Column(Float, default=0.0)