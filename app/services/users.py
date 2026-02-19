from ..repositories.users import UserRepository
from ..models import User, UserRole


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create_user(self, user) -> User | None:
        db_user = User(email=user.email, username=user.username, role=user.role)
        created_user = self.repository.create_user(db_user)
        
        return created_user
    
    def delete_user(self, user_id: int) -> None:
        self.repository.delete_user(user_id=user_id)

    def update_user(self, user_id: int, updated_user) -> User | None:
        current = self.repository.get_user_by_id(user_id)
        if current.role == UserRole.INSTRUCTOR and updated_user.role == UserRole.STUDENT and current.taught_courses:
            raise ValueError("Transition not available for instructor who managed any course")
        
        for attr, value in updated_user.model_dump(exclude_unset=True).items():
            setattr(current, attr, value)

        return self.repository.update_user(current)

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.repository.get_user_by_id(user_id)
    