import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.dependencies import get_enrollment_service
from app.mappers import db_enrollemnt_to_enrollment_details_mapper, enrollment_create_to_db_enrollment
from app.schemas import EnrollmentCreate, EnrollmentDetails, EnrollmentView
from app.services.enrollments import EnrollmentService



enrollments = APIRouter(prefix="/enrollments")

@enrollments.get("/", response_model=list[EnrollmentDetails])
def get_all_enrollments(service: Annotated[EnrollmentService, Depends(get_enrollment_service)]):
    try:
        db_enrollments = service.get_all_enrollments()
        enrollments = [db_enrollemnt_to_enrollment_details_mapper(e) for e in db_enrollments]
        
        if not enrollments:
            JSONResponse(content="No enrollments found", status_code=404)
        
        return enrollments
    except Exception as error:
        logging.error(error)
        return JSONResponse(content="Problem with retrieving enrollments from DB", status_code=500)
    
@enrollments.get("/{user_id}", response_model=list[EnrollmentDetails])
def get_enrollments_for_user(user_id: int, service: Annotated[EnrollmentService, Depends(get_enrollment_service)]):
    try:
        db_enrollments = service.get_all_enrollment_for_user(user_id)
        enrollments = [db_enrollemnt_to_enrollment_details_mapper(e) for e in db_enrollments]
        
        if not enrollments:
            JSONResponse(content="No enrollments found", status_code=404)
        
        return enrollments
    except Exception as error:
        logging.error(error)
        return JSONResponse(content="Problem with retrieving enrollments from DB", status_code=500)
    
@enrollments.post("/", response_model=EnrollmentDetails)
def create_new_enrollment(enrollment: EnrollmentCreate, service: Annotated[EnrollmentService, Depends(get_enrollment_service)]):
    try:
        db_enroll = enrollment_create_to_db_enrollment(enrollment)
        created = service.create_enrollment(db_enroll)
        return db_enrollemnt_to_enrollment_details_mapper(created)
    except Exception as error:
        logging.error(error)
        return JSONResponse(content="Problem with creating enrollment", status_code=500)
    
@enrollments.post("/{user_id}/course/{course_id}/rating/{rating}", response_model=EnrollmentDetails)
def update_course_rating(user_id: int, course_id: int, rating: int, service: Annotated[EnrollmentService, Depends(get_enrollment_service)]):
    try:
        db_enroll = service.get_enrollment(user_id, course_id)
        if not db_enroll:
            return JSONResponse(content="No enrollments found", status_code=404)
        
        updated = service.rate_course(user_id, course_id, rating)
        return db_enrollemnt_to_enrollment_details_mapper(updated)
    except Exception as error:
        logging.error(error)
        return JSONResponse(content="Problem with updating enrollment", status_code=500)
    
@enrollments.post("/{user_id}/course/{course_id}/progress/{progress}", response_model=EnrollmentDetails)
def update_course_progress(user_id: int, course_id: int, progress: int, service: Annotated[EnrollmentService, Depends(get_enrollment_service)]):
    try:
        db_enroll = service.get_enrollment(user_id, course_id)
        if not db_enroll:
            return JSONResponse(content="No enrollments found", status_code=404)
        
        updated = service.update_course_progress(user_id, course_id, progress)
        return db_enrollemnt_to_enrollment_details_mapper(updated)
    except Exception as error:
        logging.error(error)
        return JSONResponse(content="Problem with updating enrollment", status_code=500)
    