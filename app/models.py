import enum
from decimal import Decimal
from datetime import datetime
from sqlalchemy import Enum, Integer, CheckConstraint, ForeignKey, Numeric, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserRole(enum.Enum):
    STUDENT = "STUDENT"
    INSTRUCTOR = "INSTRUCTOR"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    username: Mapped[str] = mapped_column(String(120))

    role: Mapped[UserRole] = mapped_column(Enum(UserRole, native_enum=False), default=UserRole.STUDENT, nullable=False)
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="user")
    taught_courses: Mapped[list["Course"]] = relationship(back_populates="instructor")

    def __repr__(self):
        return f"User[id={self.id!r}, email={self.email!r}, username={self.username!r}]"


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    
    instructor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    instructor: Mapped["User"] = relationship(back_populates="taught_courses")

    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="course")
    modules: Mapped[list["Module"]] = relationship(back_populates="course", cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f"Course[id={self.id!r}, title={self.title!r}, description={self.description!r}, price={self.price!r}]"


class Enrollment(Base):
    __tablename__ = "enrollments"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), primary_key=True)
    enrolled_at: Mapped[datetime] = mapped_column(server_default=func.now())
    progress_percent: Mapped[int] = mapped_column(Integer, default=0)  
    is_completed: Mapped[bool] = mapped_column(default=False)
    rating: Mapped[int] = mapped_column(nullable=True)

    course: Mapped[Course] = relationship(back_populates="enrollments")
    user: Mapped[User] = relationship(back_populates="enrollments")

    __table_args__ = (
        CheckConstraint("progress_percent >= 0 AND progress_percent <= 100", name="check_progress"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating")
    )


    def __repr__(self):
        return f"Enrollment[user_id={self.user_id!r}, course_id={self.course_id!r}, enrolled_at={self.enrolled_at!r}, progress_percent={self.progress_percent!r}, is_completed={self.is_completed}]"
    

class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]

    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    course: Mapped[Course] = relationship(back_populates="modules")

    def __repr__(self):
        return f"Module[id={self.id!r}, title={self.title!r}, content={self.content!r}, course_id={self.course_id!r}]"
