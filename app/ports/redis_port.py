from abc import ABC, abstractmethod
from uuid import UUID


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

    @abstractmethod
    def delete_users_tokens(self, user_id: UUID):
        pass
