from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError
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
        try:
            user = self.db.execute(
                select(User).where(User.id == user_id)
            ).scalars().first()

            self.db.delete(user)
            self.db.commit()
        except DatabaseError:
            raise

    def get_user_by_id(self, user_id: int) -> User:
        user = self.db.execute(
            select(User).where(User.id == user_id)
        ).scalars().first()

        return user
    