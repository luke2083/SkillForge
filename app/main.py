from fastapi import FastAPI
from app.routers.courses import courses as courses_router

app = FastAPI()


app.include_router(courses_router)
