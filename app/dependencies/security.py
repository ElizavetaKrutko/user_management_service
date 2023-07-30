from datetime import datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.adapters.repositories.redis_repo import RedisRepository
from app.adapters.repositories.user.postgres_repo import SQLAlchemyUserRepository
from app.common.config import logger, settings, app_exceptions
from app.dependencies.database import get_db
from app.domain.user import User
from app.rest.routes import schemas

ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

reusable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


async def get_user_from_access_token(
        db=Depends(get_db), token: str = Depends(reusable_oauth)
):
    return await get_user_from_jwt(
        SQLAlchemyUserRepository(db),
        RedisRepository(),
        settings.jwt_access_secret_key,
        token,
    )


async def get_user_from_refresh_token(
        db=Depends(get_db), token: str = Depends(reusable_oauth)
):
    return await get_user_from_jwt(
        SQLAlchemyUserRepository(db),
        RedisRepository(),
        settings.jwt_refresh_secret_key,
        token,
    )


async def get_user_from_jwt(
        db_repo: SQLAlchemyUserRepository,
        no_sql_db_repo: RedisRepository,
        secret_key: str,
        token: str,
) -> User:
    try:
        logger.debug(token, secret_key)
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[settings.algorithm],
            options={"verify_exp": False},
        )
        token_data = schemas.TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise app_exceptions.invalid_token_error(message="Token expired", headers={"WWW-Authenticate": "Bearer"})

    except (jwt.JWTError, ValidationError):
        raise app_exceptions.no_permissions_error(message="Could not validate credentials",
                                                  headers={"WWW-Authenticate": "Bearer"})

    db_user = await db_repo.get_user_by_id(user_id=token_data.sub)

    if db_user is None:
        raise app_exceptions.no_data_error(message="Could not find user")
    else:
        if await no_sql_db_repo.check_if_jwt_blacklisted(
                token_data.sub, token_data.jwt_uuid
        ):
            raise app_exceptions.invalid_token_error(message="Token blacklisted",
                                                     headers={"WWW-Authenticate": "Bearer"})

    return db_user
