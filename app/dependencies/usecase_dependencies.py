from fastapi import Depends

from app.adapters.repositories.redis_repo import RedisRepository
from app.adapters.repositories.user.postgres_repo import \
    SQLAlchemyUserRepository
from app.dependencies.database import get_db
from app.usecases.auth import AuthManagementUseCase


def get_auth_management_use_case(db=Depends(get_db)) -> AuthManagementUseCase:
    return AuthManagementUseCase(SQLAlchemyUserRepository(db), RedisRepository())
