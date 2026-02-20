from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.repositories.courses import CourseRepository
from app.repositories.users import UserRepository
from app.services.courses import CourseService
from app.services.users import UserService


def get_user_repository(db: Annotated[Session, Depends(get_db)]) -> UserRepository:
    return UserRepository(db)

def get_course_repository(db: Annotated[Session, Depends(get_db)]) -> CourseRepository:
    return CourseRepository(db)

def get_course_service(
        course_repository: Annotated[CourseRepository, Depends(get_course_repository)],
        user_repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> CourseService:
    return CourseService(course_repository, user_repository)

def get_user_service(user_repository: Annotated[UserRepository, Depends(get_user_repository)]) -> UserService:
    return UserService(user_repository)

