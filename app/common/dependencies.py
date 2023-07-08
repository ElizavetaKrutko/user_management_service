from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common import security
from app.common.config import settings
from app.crud import crud
from app.rest.schemas import TokenPayload, UserRead

# from app.db.dependencies.database import async_session


# import redis


"""def create_redis():
    return redis.ConnectionPool(
        host='redis',
        port=6379,
        db=0,
        decode_responses=True
    ) 


def get_redis():
    return redis.Redis(connection_pool=create_redis(), decode_responses=True) """


reusable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


def get_current_user(
    db: AsyncSession = Depends(get_session), token: str = Depends(reusable_oauth)
) -> UserRead:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[security.ALGORITHM],
            options={"verify_exp": False},
        )
        token_data = TokenPayload(**payload)

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

    db_user = crud.get_user_by_username(db, username=token_data.sub)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return UserRead.from_orm(db_user)


# разобраться с ролями - передавать внутрь группу того юзера, ид которого пробарасывается в эндпоинт - ????
def is_superuser(user: UserRead = Depends(get_current_user)):
    if user.is_superuser:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No permissions",
        )
