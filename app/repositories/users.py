from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    
    def delete_user(self, user_id: int) -> bool:
        user = self.db.execute(
            select(User).where(User.id == user_id)
        ).scalars().first()

        if user:
            self.db.delete(user)
            self.db.commit()
            return True

    def update_user(self, user: User) -> User | None:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_user_by_id(self, user_id: int) -> User:
        user = self.db.execute(
            select(User).where(User.id == user_id).options(selectinload(User.taught_courses))
        ).scalars().first()

        return user
    
    def get_all_users(self) -> list[User]:
        return self.db.get(User)
    

    def get_user_by_email(self, email: str) -> User | None:
        user = self.db.execute(
            select(User).where(User.email == email)
        ).scalars().first()

        return user
    