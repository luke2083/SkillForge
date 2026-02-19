from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from ..models import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    
    def delete_user(self, user_id: int) -> None:
        user = self.db.execute(
            select(User).where(User.id == user_id)
        ).scalars().first()

        if user:
            self.db.delete(user)
            self.db.commit()

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
    