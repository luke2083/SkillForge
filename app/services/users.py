from ..repositories.users import UserRepository
from ..models import User


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create_user(self, user) -> User:
        db_user = User(email=user.email, username=user.username, role=user.role)
        created_user = self.repository.create_user(db_user)
        
        return created_user
    
    def delete_user(self, user_id: int) -> None:
        self.repository.delete_user(user_id=user_id)

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.repository.get_user_by_id(user_id)
    