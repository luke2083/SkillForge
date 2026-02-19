from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload

from ..models import Enrollment


class EnrollmentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_enrollment(self, user_id: int, course_id: int) -> Enrollment:
        enrollment = Enrollment(user_id=user_id, course_id=course_id)
        
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)

        return enrollment
    
    def get_all_enrollments_for_user_id(self, user_id: int) -> list[Enrollment]:
        enrollments = self.db.execute(
            select(Enrollment).where(Enrollment.user_id == user_id).options(joinedload(Enrollment.course))
        ).scalars().all()

        return enrollments

    def get_enrollment(self, user_id: int, course_id: int) -> Enrollment | None:
        enrollment = self.db.get(Enrollment, (user_id, course_id))
        return enrollment
    
    def update_enrollment(self, enrollment: Enrollment) -> Enrollment:
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)

        return enrollment
    