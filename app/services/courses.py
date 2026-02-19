from app.exceptions import PriceTooLowError
from app.repositories.courses import CourseRepository
from app.models import Course
from app.repositories.users import UserRepository
from app.schemas import CourseCreate

class CourseService:
    def __init__(self, course_repository: CourseRepository, user_repository: UserRepository) -> None:
        self.course_repository = course_repository
        self.user_repository = user_repository

    def create_course(self, course: CourseCreate) -> Course | None:
        user = self.user_repository.get_user_by_id(course.instructor_id)

        if user.role != "instructor":
            raise ValueError("Only instructor can create the course")
        
        if course.price > 0 and course.price < 10:
            raise PriceTooLowError("The minimum price of the course is 10")
        
        db_course = Course(
            title=course.title,
            description=course.description,
            price=course.price,
            instructor_id=course.instructor_id
        )

        return self.course_repository.create_course(db_course)
    
    def delete_course(self, course_id: int) -> None:
        self.course_repository.delete_course(course_id)

    def get_course_by_id(self, course_id: int) -> Course | None:
        return self.course_repository.get_course_by_id(course_id)
    
    def get_courses_with_details(self) -> list[Course] | None:
        return self.course_repository.get_all_courses_with_details()
