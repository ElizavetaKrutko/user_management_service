from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.group import Group
from app.domain.user import User


class NoSqlDBRepositoryPort(ABC):
    @abstractmethod
    async def activate_jwt(self, user_id: UUID, jwt_uuid: UUID):
        pass

    @abstractmethod
    async def check_if_jwt_blacklisted(self, user_id: UUID, jwt_uuid: UUID):
        pass

    @abstractmethod
    async def blacklist_jwt(self, user_id: UUID):
        pass
