from fastapi import Depends

from app.adapters.repositories.amazon_repo import AmazonRepository
from app.adapters.repositories.redis_repo import RedisRepository
from app.adapters.repositories.user.postgres_repo import SQLAlchemyUserRepository
from app.common.config import app_exceptions
from app.dependencies.database import get_db
from app.usecases.auth import AuthManagementUseCase
from app.usecases.user import UserUseCase


def get_auth_management_use_case(db=Depends(get_db)) -> AuthManagementUseCase:
    return AuthManagementUseCase(
        SQLAlchemyUserRepository(db),
        RedisRepository(),
        AmazonRepository(),
        app_exceptions,
    )


def get_user_management_use_case(db=Depends(get_db)) -> UserUseCase:
    return UserUseCase(SQLAlchemyUserRepository(db), RedisRepository(), app_exceptions)
