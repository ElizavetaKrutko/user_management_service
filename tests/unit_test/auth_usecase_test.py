import uuid
from datetime import datetime

import pytest
from jose import jwt

from app.common.config import app_exceptions, settings
from app.common.exceptions.fast_api_sql_alchemy_exceptions import (
    AppExceptions, BadRequestError)
from app.domain.user import Role, User
from app.usecases.auth import AuthManagementUseCase
from tests.unit_test.mocks.inmemory_postgres_repo import InMemoryUserRepository
from tests.unit_test.mocks.inmemory_redis_repo import InMemoryRedisRepository


@pytest.fixture
def test_sql_repository():
    return InMemoryUserRepository()


@pytest.fixture
def test_nosql_repository():
    return InMemoryRedisRepository()


@pytest.fixture
def test_cloud_repository():
    return AppExceptions()


@pytest.fixture
def exceptions():
    return app_exceptions


@pytest.fixture
def auth_use_case(
    test_sql_repository, test_nosql_repository, test_cloud_repository, exceptions
):
    return AuthManagementUseCase(
        test_sql_repository, test_nosql_repository, test_cloud_repository, exceptions
    )


def test_create_access_token_success(auth_use_case):
    user_id = "32d8790f-bce9-430e-ad70-b8a410cd66e9"
    jwt_uuid = uuid.uuid4()
    token = auth_use_case.create_access_token(user_id, jwt_uuid)
    assert token is not None


def test_create_refresh_token_success(auth_use_case):
    user_id = "32d8790f-bce9-430e-ad70-b8a410cd66e9"
    jwt_uuid = uuid.uuid4()
    token = auth_use_case.create_refresh_token(user_id, jwt_uuid)
    payload = jwt.decode(
        token,
        settings.jwt_refresh_secret_key,
        algorithms=[settings.algorithm],
        options={"verify_exp": False},
    )
    assert payload["sub"] == user_id


@pytest.mark.asyncio
async def test_create_user_success(auth_use_case):
    new_user_data = User(
        role=Role.MODERATOR,
        name="elizaveta",
        surname="krutsko",
        username="lizakrutsko",
        email="lizaliza@mail.ru",
        group_id=1,
        is_blocked=False,
        created_at=datetime.now(),
    )
    token_pair = await auth_use_case.create_user(new_user_data)
    assert token_pair["access_token"] != ""


@pytest.mark.asyncio
async def test_create_user_duplicate_username(auth_use_case):
    new_user_data = User(
        role=Role.MODERATOR,
        name="elizaveta",
        surname="krutsko",
        username="anna123",
        email="lizaliza@mail.ru",
        group_id=1,
        is_blocked=False,
        created_at=datetime.now(),
    )
    with pytest.raises(BadRequestError) as error:
        await auth_use_case.create_user(new_user_data)
    assert str(error.value.args[0]) == "User with provided user name already exists!"


@pytest.mark.asyncio
async def test_create_user_duplicate_email(auth_use_case):
    new_user_data = User(
        role=Role.MODERATOR,
        name="elizaveta",
        surname="krutsko",
        username="lizakrutsko",
        email="ekaterina123.@gmail.com",
        group_id=1,
        is_blocked=False,
        created_at=datetime.now(),
    )
    with pytest.raises(BadRequestError) as error:
        await auth_use_case.create_user(new_user_data)
    assert str(error.value.args[0]) == "User with provided email already exists!"


@pytest.mark.asyncio
async def test_login_user_incorrect_login(auth_use_case):
    user_data = User(login="ekaterina1234", password="lizavetaaa")
    with pytest.raises(BadRequestError) as error:
        await auth_use_case.login_user(user_data)
    assert str(error.value.args[0]) == "Incorrect login"


@pytest.mark.asyncio
async def test_login_user_incorrect_password(auth_use_case):
    user_data = User(login="ekaterina123", password="lizavetaaaa")
    with pytest.raises(BadRequestError) as error:
        await auth_use_case.login_user(user_data)
    assert str(error.value.args[0]) == "Incorrect password"


@pytest.mark.asyncio
async def test_login_user_is_blocked(auth_use_case):
    user_data = User(login="ekaterina123", password="lizavetaaa")
    with pytest.raises(BadRequestError) as error:
        await auth_use_case.login_user(user_data)
    assert str(error.value.args[0]) == "User is blocked"
