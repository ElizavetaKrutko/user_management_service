import uuid

import aioredis

from app.common.config import logger
from app.ports.redis_port import NoSqlDBRepositoryPort


class RedisRepository(NoSqlDBRepositoryPort):
    def __init__(self) -> None:
        self.redis = aioredis.from_url(
            "redis://redis:6379", encoding="utf-8", decode_responses=True
        )

    async def activate_jwt(self, user_id, jwt_uuid):
        # just for logging
        logger.debug("we are on activate_jwt")
        logger.debug("jwt_uuid: ")
        logger.debug(jwt_uuid)

        logger.debug("user_id: ")
        logger.debug(user_id)

        user_active_jwt_key = str(user_id) + ":active_jwt"
        user_blacklist_key = str(user_id) + ":blacklist"

        current_active_jwt = await self.redis.get(user_active_jwt_key)
        logger.debug("current_active_jwt: ")
        logger.debug(current_active_jwt)

        if current_active_jwt:
            token_to_blacklist = await self.redis.lpush(
                user_blacklist_key, current_active_jwt
            )
            logger.debug("count tokens in blacklist: ")
            logger.debug(token_to_blacklist)

        new_active_token = await self.redis.set(user_active_jwt_key, str(jwt_uuid))
        logger.debug("new_active_token: ")
        logger.debug(new_active_token)

        # just for logging
        current_user_active_jwt = await self.redis.get(user_active_jwt_key)
        logger.debug("current_user_active_jwt: ")
        logger.debug(current_user_active_jwt)

        # just for logging
        user_blacklist_all = await self.redis.lrange(user_blacklist_key, 0, -1)
        logger.debug("user_blacklist_all: ")
        logger.debug(user_blacklist_all)

        await self.redis.close()

    async def check_if_jwt_blacklisted(self, user_id, jwt_uuid):
        # just for logging
        logger.debug("we are on check_if_jwt_blacklisted")

        user_blacklist: str = str(user_id) + ":blacklist"

        user_blacklist_all = await self.redis.lrange(user_blacklist, 0, -1)
        logger.debug("user_blacklist_all: ")
        logger.debug(user_blacklist_all)

        result: bool = False

        if str(jwt_uuid) in user_blacklist_all:
            result = True

        await self.redis.close()

        logger.debug(result)

        return result

    async def blacklist_jwt(self, user_id):
        # just for logging
        logger.debug("we are on blacklist_jwt")
        logger.debug(user_id)

        user_active_jwt_key = str(user_id) + ":active_jwt"
        user_blacklist = str(user_id) + ":blacklist"

        current_active_token = await self.redis.get(user_active_jwt_key)
        logger.debug("current_active_token: ")
        logger.debug(current_active_token)

        token_to_blacklist = await self.redis.lpush(
            user_blacklist, current_active_token
        )
        logger.debug("token_to_blacklist: ")
        logger.debug(token_to_blacklist)

        await self.redis.delete(user_active_jwt_key)

        # just for logging
        current_active_token = await self.redis.get(user_active_jwt_key)
        logger.debug("current_active_token: ")
        logger.debug(current_active_token)

        # just for logging
        user_blacklist_all = await self.redis.lrange(user_blacklist, 0, -1)
        logger.debug("user_blacklist_all: ")
        logger.debug(user_blacklist_all)

        await self.redis.close()

    async def delete_users_tokens(self, user_id):
        # just for logging
        logger.debug("we are on delete_users_tokens")
        logger.debug(user_id)

        user_active_jwt_key = str(user_id) + ":active_jwt"
        user_blacklist = str(user_id) + ":blacklist"

        await self.redis.delete(user_active_jwt_key)
        await self.redis.delete(user_blacklist)

        # just for logging
        current_active_token = await self.redis.get(user_active_jwt_key)
        logger.debug("current_active_token: ")
        logger.debug(current_active_token)

        # just for logging
        user_blacklist_all = await self.redis.lrange(user_blacklist, 0, -1)
        logger.debug("user_blacklist_all: ")
        logger.debug(user_blacklist_all)

        await self.redis.close()

    async def save_reset_password_token(self, user_id: uuid.UUID, token: str):
        reset_password_token_key = str(user_id) + ":reset_password_token"
        reset_password_token = await self.redis.set(reset_password_token_key, token)
        await self.redis.expire(reset_password_token_key, 600)
        logger.debug(reset_password_token)
        await self.redis.close()

    async def get_reset_password_token(self, user_id: uuid.UUID):
        reset_password_token_key = str(user_id) + ":reset_password_token"
        reset_password_token = await self.redis.get(reset_password_token_key)
        logger.debug(reset_password_token)
        await self.redis.close()
        return reset_password_token
