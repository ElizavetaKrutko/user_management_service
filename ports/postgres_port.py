from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.group import Group
from app.domain.user import User


class PostgresRepositoryPort(ABC):
    @abstractmethod
    # TODO: add input parameters, annotation
    async def create_user(self) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    async def get_user_by_login(self, username, email=None, phone_number=None):
        pass

    @abstractmethod
    async def get_groups(self):
        pass
