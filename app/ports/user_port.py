from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.user import User


class UserRepositoryPort(ABC):
    @abstractmethod
    # TODO: add input parameters, annotation
    async def create_user(self, new_user_data: User) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    async def get_user_by_login(self, username, email=None, phone_number=None):
        pass
