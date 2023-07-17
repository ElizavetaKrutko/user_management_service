import logging
from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.adapters.repositories.redis_repo import RedisRepository
from app.adapters.repositories.user.postgres_repo import \
    SQLAlchemyUserRepository
from app.common.config import settings
from app.dependencies.database import get_db
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
) -> schemas.UserBaseRead:
    try:
        logging.debug(token, secret_key)
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[settings.algorithm],
            options={"verify_exp": False},
        )
        token_data = schemas.TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db_user = await db_repo.get_user_by_id(user_id=token_data.sub)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    else:
        if await no_sql_db_repo.check_if_jwt_blacklisted(
            token_data.sub, token_data.jwt_uuid
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token blacklisted",
                headers={"WWW-Authenticate": "Bearer"},
            )

    return schemas.UserBaseRead.from_orm(db_user)
