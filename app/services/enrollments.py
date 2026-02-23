from app.exceptions import CourseNotCompletedError, InvalidProgressError, InvalidRatingError

from app.repositories.enrollments import EnrollmentRepository
from app.models import Enrollment


class EnrollmentService:
    def __init__(self, repository: EnrollmentRepository) -> None:
        self.repository = repository

    def create_enrollment(self, user_id: int, course_id: int) -> Enrollment:
        enrollment = self.repository.get_enrollment(user_id, course_id)

        if not enrollment:
            enrollment = self.repository.create_enrollment(user_id, course_id)

        return enrollment
    
    def get_all_enrollment_for_user(self, user_id: int) -> list[Enrollment] | None:
        enrollments = self.repository.get_all_enrollments_for_user_id(user_id)
        return enrollments
    
    def get_all_enrollments(self) -> list[Enrollment] | None:
        return self.repository.get_all_enrollments()
    
    def get_enrollment(self, user_id: int, course_id: int) -> Enrollment | None:
        return self.repository.get_enrollment(user_id, course_id)
    
    def update_course_progress(self, user_id: int, course_id: int, progress: int) -> Enrollment | None:
        if progress < 0 or progress > 100:
            raise InvalidProgressError("Progress must be in the range 0 - 100")
        
        enrollment = self.repository.get_enrollment(user_id, course_id)

        if not enrollment:
            raise ValueError("Enrollment not found")

        if progress < enrollment.progress_percent:
            raise InvalidProgressError("New progress must be greater then current progress")
        
        if progress == 100:
            enrollment.is_completed = True
        
        enrollment.progress_percent = progress
        return self.repository.update_enrollment(enrollment)
    
    def rate_course(self, user_id: int, course_id: int, rating: int) -> Enrollment | None:
        if rating < 1 or rating > 5:
            raise InvalidRatingError("Rating must be in the range 1 - 5")
        
        enrollment = self.repository.get_enrollment(user_id, course_id)

        if not enrollment.is_completed:
            raise CourseNotCompletedError()
        
        enrollment.rating = rating
        return self.repository.update_enrollment(enrollment)
