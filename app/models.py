import enum
from datetime import datetime
from sqlalchemy import Enum, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserRole(enum.Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    username: Mapped[str]

    role: Mapped[UserRole] = mapped_column(Enum(UserRole, native_enum=False), default=UserRole.STUDENT, nullable=False)
    enrollments: Mapped["Enrollment"] = relationship(back_populates="user")
    taught_courses: Mapped["Course"] = relationship(back_populates="instructor")

    def __repr__(self):
        return f"User[id={self.id!r}, email={self.email!r}, username={self.username!r}]"


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]

    enrollments: Mapped["Enrollment"] = relationship(back_populates="course")
    
    instructor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    instructor: Mapped["User"] = relationship(back_populates="taught_courses")

    def __repr__(self):
        return f"Course[id={self.id!r}, title={self.title!r}, description={self.description!r}, price={self.price!r}]"


class Enrollment(Base):
    __tablename__ = "enrollments"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    enrolled_at: Mapped[datetime]
    progress_percent: Mapped[int] = mapped_column(Integer, CheckConstraint("progress_percent >= 0 and progress_percent <= 100"))  
    is_completed: Mapped[bool]
    rating: Mapped[int] = mapped_column(CheckConstraint("rating >= 1 and rating <= 5"), nullable=True)

    course: Mapped[Course] = relationship(back_populates="enrollments")
    user: Mapped[User] = relationship(back_populates="enrollments")


    def __repr__(self):
        return f"Enrollment[user_id={self.user_id!r}, course_id={self.course_id!r}, enrolled_at={self.enrolled_at!r}, progress_percent={self.progress_percent!r}, is_completed={self.is_completed}]"
    
    