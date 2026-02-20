from app.models import Course
from app.schemas import CourseCreate, CourseDetails, EnrollmentView, ModuleView, UserView


def db_course_to_course_details_mapper(db_course: Course) -> CourseDetails:
    return CourseDetails(
            id=db_course.id,
            title=db_course.title,
            description=db_course.description,
            price=db_course.price,
            instructor=UserView(
                id=db_course.instructor.id,
                email=db_course.instructor.email,
                username=db_course.instructor.username,
                role=db_course.instructor.role
            ),
            enrollments=[
                EnrollmentView(
                    user_id=db_enroll.user_id,
                    course_id=db_enroll.course_id,
                    enrolled_at=db_enroll.enrolled_at,
                    progress_percent=db_enroll.progress_percent,
                    is_completed=db_enroll.is_completed,
                    rating=db_enroll.rating,
                    user=UserView(
                        id=db_enroll.user.id,
                        email=db_enroll.user.email,
                        username=db_enroll.user.username,
                        role=db_enroll.user.role
                    )
                ) for db_enroll in db_course.enrollments
            ] if db_course.enrollments else None,
            modules=[
                ModuleView(
                    id=db_module.id,
                    title=db_module.title,
                    content=db_module.content
                ) for db_module in db_course.modules
            ] if db_course.modules else None
        )

def course_create_to_db_course_mapper(course_create: CourseCreate) -> Course:
    return Course(
        title=course_create.title,
        description=course_create.description,
        price=course_create.price,
        instructor_id=course_create.instructor_id
    )
    