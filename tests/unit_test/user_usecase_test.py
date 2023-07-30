import uuid
from datetime import datetime

import pytest

from app.adapters.repositories.inmemory_redis_repo import \
    InMemoryRedisRepository
from app.adapters.repositories.user.inmemory_postgres_repo import \
    InMemoryUserRepository
from app.domain.user import Role, User
from app.usecases.user import UserUseCase


@pytest.fixture
def user_sql_repository():
    return InMemoryUserRepository()


@pytest.fixture
def user_nosql_repository():
    return InMemoryRedisRepository()


@pytest.fixture
def user_use_case(user_sql_repository, user_nosql_repository):
    return UserUseCase(user_sql_repository, user_nosql_repository)


@pytest.mark.asyncio
async def test_user_create_success(user_use_case):
    user = User(
        password="lalala222",
        role=Role.USER,
        name="elizaveta",
        surname="krutsko",
        username="lizakrutsko",
        email="lizaliza@mail.ru",
        group_id=1,
        is_blocked=False,
        created_at=datetime.now(),
    )
    db_user = await user_use_case.patch_user(user, uuid.uuid4())
    assert isinstance(db_user, User)
