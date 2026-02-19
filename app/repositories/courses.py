from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import DatabaseError

from ..models import Course


class CourseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_course(self, course: Course) -> Course:
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)

        return course
    
    def delete_course(self, course_id: int) -> None:
        course = self.db.execute(
            select(Course).where(Course.id == course_id)
        ).scalars().first()
            
        if course:
            self.db.delete(course)
            self.db.commit()

    def get_course_by_id(self, course_id: int) -> Course:
        course = self.db.execute(
            select(Course).where(Course.id == course_id)
        ).scalars().first()

        return course
    
    def get_all_courses_with_details(self) -> list[Course]:
        courses = self.db.execute(
            select(Course).options(selectinload(Course.enrollments), selectinload(Course.modules))
        ).scalars().all()

        return courses

