from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.group import Group
from app.domain.user import User


class RedisRepositoryPort(ABC):
    @abstractmethod
    async def activate_jwt(self, user_id, jwt_uuid):
        pass

    @abstractmethod
    async def check_if_jwt_blacklisted(self, user_id, jwt_uuid):
        pass

    @abstractmethod
    async def blacklist_jwt(self, user_id):
        pass
