from pydantic import BaseModel
from decimal import Decimal


class CourseCreate(BaseModel):
    title: str
    description: str
    price: Decimal
    instructor_id: int
    