from .models import Base, User, Course, Enrollment, UserRole
from .database import engine
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, joinedload
from datetime import datetime, timezone


Base.metadata.create_all(engine)

with Session(engine) as session:
    e = session.execute(
        select(Enrollment).options(joinedload(Enrollment.course), joinedload(Enrollment.user))
    ).scalars().first()

    print(e.user)
    