from fastapi import FastAPI
from app.routers.courses import courses as courses_router
from app.routers.users import users as users_router
from app.routers.enrollments import enrollments as enrollments_router

app = FastAPI()


app.include_router(courses_router)
app.include_router(users_router)
app.include_router(enrollments_router)
