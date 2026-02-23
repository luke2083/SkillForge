import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.mappers import db_user_to_user_view_mapper, user_create_to_db_user_mapper
from app.schemas import UserCreate, UserView
from app.dependencies import get_user_service
from app.services.users import UserService


users = APIRouter(prefix='/users', tags=['users'])

@users.get("/", response_model=UserView)
def get_all_users(service: Annotated[UserService, Depends(get_user_service)]):
    return service.get_all_users()


@users.get("/{user_id}", response_model=UserView)
def get_user_by_id(user_id: int, service: Annotated[UserService, Depends(get_user_service)]):
    try:
        user = service.get_user_by_id(user_id)

        if not user:
            return JSONResponse(content=f"User {user_id} not found", status_code=404)
    except Exception as error:
        logging.error(error)
        return JSONResponse(content="Problem with getting user", status_code=500)
    
    return user


@users.post("/", response_model=UserView)
def create_user(user: UserCreate, service: Annotated[UserService, Depends(get_user_service)]):
    if service.get_user_by_email(user.email):
        return JSONResponse(content="User already exists", status_code=422)
    
    try:
        db_user = user_create_to_db_user_mapper(user)
        created = service.create_user(db_user)

        return db_user_to_user_view_mapper(created)
    except Exception as error:
        logging.error(error)
        return JSONResponse(content="Problem with creating new user", status_code=500)
    
    
@users.delete("/{user_id}")
def delete_user_by_id(user_id: int, service: Annotated[UserService, Depends(get_user_service)]):
    try:
        if not service.delete_user(user_id):
            return JSONResponse(content="User doesn't exists", status_code=404)
        else:
            JSONResponse(content=f"User {user_id} deleted", status_code=200)

    except Exception as error:
        logging.error(error)
        return JSONResponse(content=f"Problem with deleting user {user_id}", status_code=500)
    