from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Annotated

from app.dependencies import get_course_service, get_user_service
from app.services.courses import CourseService
from app.schemas import CourseCreate, CourseView, CourseDetails, UserView, EnrollmentView, ModuleView
from app.mappers import course_create_to_db_course_mapper, db_course_to_course_details_mapper


courses = APIRouter(prefix="/courses", tags=["courses"])

@courses.get("/", response_model=list[CourseDetails])
def get_all_courses(service: Annotated[CourseService, Depends(get_course_service)]):
    db_courses = service.get_courses_with_details()
    courses = []

    for db_course in db_courses:
        course = db_course_to_course_details_mapper(db_course)
        courses.append(course)

    return courses


@courses.post("/", response_model=CourseDetails)
def create_new_course(course: CourseCreate, service: Annotated[CourseService, Depends(get_course_service)]):
    db_course = service.create_course(course_create_to_db_course_mapper(course))

    if db_course:
        return db_course_to_course_details_mapper(db_course)


@courses.get("/{course_id}", response_model=CourseDetails)
def get_course_by_id(course_id: int, service: Annotated[CourseService, Depends(get_course_service)]):
    db_course = service.get_course_by_id(course_id)

    if db_course:
        return db_course_to_course_details_mapper(db_course)
    
    return JSONResponse(content="Course not found", status_code=404)


@courses.delete("/{course_id}")
def delete_course_by_id(course_id: int, service: Annotated[CourseService, Depends(get_course_service)]):
    try:
        service.delete_course(course_id)
        return JSONResponse(content=f"Course {course_id} deleted", status_code=200)
    except Exception:
        return JSONResponse(content="Problem with deleting the course", status_code=500)
    