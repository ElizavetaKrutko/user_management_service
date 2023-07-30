import uuid

from app.common.config import logger
from app.ports.redis_port import NoSqlDBRepositoryPort


class InMemoryRedisRepository(NoSqlDBRepositoryPort):
    def __init__(self):
        self.redis_storage = {}

    # все методы переписать!!!!

    async def activate_jwt(self, user_id, jwt_uuid):
        user_active_jwt_key = str(user_id) + ":active_jwt"
        user_blacklist_key = str(user_id) + ":blacklist"

        current_active_jwt = await self.redis.get(user_active_jwt_key)

        if current_active_jwt:
            token_to_blacklist = await self.redis.lpush(
                user_blacklist_key, current_active_jwt
            )

        new_active_token = await self.redis.set(user_active_jwt_key, str(jwt_uuid))

    async def check_if_jwt_blacklisted(self, user_id, jwt_uuid):
        user_blacklist: str = str(user_id) + ":blacklist"

        user_blacklist_all = await self.redis.lrange(user_blacklist, 0, -1)

        result: bool = False

        if str(jwt_uuid) in user_blacklist_all:
            result = True

        return result

    async def blacklist_jwt(self, user_id):
        user_active_jwt_key = str(user_id) + ":active_jwt"
        user_blacklist = str(user_id) + ":blacklist"

        current_active_token = await self.redis.get(user_active_jwt_key)

        token_to_blacklist = await self.redis.lpush(
            user_blacklist, current_active_token
        )

        await self.redis.delete(user_active_jwt_key)

    async def delete_users_tokens(self, user_id):
        user_active_jwt_key = str(user_id) + ":active_jwt"
        user_blacklist = str(user_id) + ":blacklist"

        await self.redis.delete(user_active_jwt_key)
        await self.redis.delete(user_blacklist)

    async def save_reset_password_token(self, user_id: uuid.UUID, token: str):
        reset_password_token_key = str(user_id) + ":reset_password_token"
        reset_password_token = await self.redis.set(reset_password_token_key, token)
        await self.redis.expire(reset_password_token_key, 600)

    async def get_reset_password_token(self, user_id: uuid.UUID):
        reset_password_token_key = str(user_id) + ":reset_password_token"
        reset_password_token = await self.redis.get(reset_password_token_key)
        return reset_password_token
