import logging

import aioredis


class RedisRepository:
    def __init__(self) -> None:
        self.redis = aioredis.from_url(
            "redis://redis:6379", encoding="utf-8", decode_responses=True
        )

    async def activate_jwt(self, user_id, jwt_uuid):
        # just for logging
        logging.error("we are on activate_jwt")
        logging.error("jwt_uuid: ")
        logging.error(jwt_uuid)

        user_active_jwt_key = str(user_id) + ":active_jwt"
        user_blacklist_key = str(user_id) + ":blacklist"

        current_active_jwt = await self.redis.get(user_active_jwt_key)
        logging.error("current_active_jwt: ")
        logging.error(current_active_jwt)

        if current_active_jwt:
            token_to_blacklist = await self.redis.lpush(
                user_blacklist_key, current_active_jwt
            )
            logging.error("count tokens in blacklist: ")
            logging.error(token_to_blacklist)

        new_active_token = await self.redis.set(user_active_jwt_key, jwt_uuid)
        logging.error("new_active_token: ")
        logging.error(new_active_token)

        # just for logging
        current_user_active_jwt = await self.redis.get(user_active_jwt_key)
        logging.error("current_user_active_jwt: ")
        logging.error(current_user_active_jwt)

        # just for logging
        user_blacklist_all = await self.redis.lrange(user_blacklist_key, 0, -1)
        logging.error("user_blacklist_all: ")
        logging.error(user_blacklist_all)

        await self.redis.close()

    async def check_if_jwt_blacklisted(self, user_id, jwt_uuid):
        # just for logging
        logging.error("we are on check_if_jwt_blacklisted")

        user_blacklist: str = str(user_id) + ":blacklist"

        user_blacklist_all = await self.redis.lrange(user_blacklist, 0, -1)
        logging.error("user_blacklist_all: ")
        logging.error(user_blacklist_all)

        result: bool = False

        if jwt_uuid in user_blacklist_all:
            result = True

        await self.redis.close()

        logging.error(result)

        return result

    async def blacklist_jwt(self, user_id):
        # just for logging
        logging.error("we are on blacklist_jwt")
        logging.error(user_id)

        user_active_jwt_key = str(user_id) + ":active_jwt"
        user_blacklist = str(user_id) + ":blacklist"

        current_active_token = await self.redis.get(user_active_jwt_key)
        logging.error("current_active_token: ")
        logging.error(current_active_token)

        token_to_blacklist = await self.redis.lpush(
            user_blacklist, current_active_token
        )
        logging.error("token_to_blacklist: ")
        logging.error(token_to_blacklist)

        await self.redis.delete(user_active_jwt_key)

        # just for logging
        current_active_token = await self.redis.get(user_active_jwt_key)
        logging.error("current_active_token: ")
        logging.error(current_active_token)

        # just for logging
        user_blacklist_all = await self.redis.lrange(user_blacklist, 0, -1)
        logging.error("user_blacklist_all: ")
        logging.error(user_blacklist_all)

        await self.redis.close()
