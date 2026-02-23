from fastapi import FastAPI
from app.routers.courses import courses as courses_router
from app.routers.users import users as users_router

app = FastAPI()


app.include_router(courses_router)
