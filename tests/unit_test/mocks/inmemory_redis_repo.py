import uuid

from app.ports.redis_port import NoSqlDBRepositoryPort


class InMemoryRedisRepository(NoSqlDBRepositoryPort):
    def __init__(self):
        self.redis_storage = []

    async def activate_jwt(self, user_id, jwt_uuid):
        pass

    async def check_if_jwt_blacklisted(self, user_id, jwt_uuid):
        pass

    async def blacklist_jwt(self, user_id):
        pass

    async def delete_users_tokens(self, user_id):
        pass

    async def save_reset_password_token(self, user_id: uuid.UUID, token: str):
        pass

    async def get_reset_password_token(self, user_id: uuid.UUID):
        pass
