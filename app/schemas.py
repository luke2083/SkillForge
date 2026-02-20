from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

from app.models import UserRole


class CourseCreate(BaseModel):
    title: str
    description: str
    price: Decimal
    instructor_id: int
    
class CourseView(CourseCreate):
    id: int

class CourseDetails(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    instructor: "UserView"
    enrollments: list["EnrollmentView"] | None = None
    modules: list["ModuleView"] | None = None


class UserView(BaseModel):
    id: int
    email: str
    username: str
    role: UserRole

class EnrollmentView(BaseModel):
    user_id: int
    course_id: int
    enrolled_at: datetime
    progress_percent: int | None = None
    is_completed: bool
    rating: int | None = None
    user: UserView

class ModuleView(BaseModel):
    id: int
    title: str
    content: str
