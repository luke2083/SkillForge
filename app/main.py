from .models import Base, User, Course, Enrollment, UserRole
from .database import engine, get_db


# Base.metadata.create_all(engine)

# with Session(engine) as session:
#     e = session.execute(
#         select(Enrollment).options(joinedload(Enrollment.course), joinedload(Enrollment.user))
#     ).scalars().first()

#     print(e.user)
    
from app.repositories.enrollments import EnrollmentRepository


er = EnrollmentRepository(db=next(get_db()))
eee = er.get_enrollment(8, 2)
print(eee)