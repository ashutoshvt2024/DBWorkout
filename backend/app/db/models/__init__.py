# Import the Base class
from app.db.base import Base

# Import all models here to ensure they are registered with Base.metadata
from app.db.models.user import User
from app.db.models.course import Course
from app.db.models.session import Session
from app.db.models.enrollment import Enrollment
from app.db.models.task import Task
from app.db.models.submission import Submission
from app.db.models.assignment import Assignment
from app.db.models.task_time_tracking import TaskTimeTracking
from app.db.models.schema import Schema
