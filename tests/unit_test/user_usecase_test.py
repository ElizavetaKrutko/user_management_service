from datetime import datetime

import pytest

from app.common.config import app_exceptions
from app.common.exceptions.base_exceptions import BaseAppExceptions
from app.common.exceptions.fast_api_sql_alchemy_exceptions import (
    NoDataError,
    NoPermissionsError,
)
from app.domain.user import Role, User
from app.usecases.user import UserUseCase
from tests.unit_test.mocks.inmemory_postgres_repo import InMemoryUserRepository
from tests.unit_test.mocks.inmemory_redis_repo import InMemoryRedisRepository


@pytest.fixture
def user_sql_repository():
    return InMemoryUserRepository()


@pytest.fixture
def user_nosql_repository():
    return InMemoryRedisRepository()


@pytest.fixture
def user_exceptions() -> BaseAppExceptions:
    return app_exceptions


@pytest.fixture
def user_use_case(user_sql_repository, user_nosql_repository, user_exceptions):
    return UserUseCase(user_sql_repository, user_nosql_repository, user_exceptions)


@pytest.mark.asyncio
async def test_user_patch_success(user_use_case):
    user = User(
        role=Role.USER,
        name="elizaveta",
        surname="krutsko",
        username="lizakrutsko",
        email="lizaliza@mail.ru",
        group_id=1,
        is_blocked=False,
        created_at=datetime.now(),
    )
    user_id = "c43358e3-3846-45e6-9901-25e23fc836a7"
    db_user = await user_use_case.patch_user(user, user_id)
    assert db_user["name"] == "elizaveta"


@pytest.mark.asyncio
async def test_get_another_user_by_id_no_data_error(user_use_case):
    user_id_needed = "32d8790f-bce9-430e-ad70-b8a410cd66e"
    user_data = User(role=Role.ADMIN, group_id=1)
    with pytest.raises(NoDataError) as error:
        await user_use_case.get_another_user_by_id(user_id_needed, user_data)
    assert str(error.value.args[0]) == "Could not find user"


@pytest.mark.asyncio
async def test_get_another_user_by_id_no_permission_error(user_use_case):
    user_id_needed = "32d8790f-bce9-430e-ad70-b8a410cd66e9"
    user_data = User(role=Role.USER, group_id=1)
    with pytest.raises(NoPermissionsError) as error:
        await user_use_case.get_another_user_by_id(user_id_needed, user_data)
    assert str(error.value.args[0]) == "No permissions"


@pytest.mark.asyncio
async def test_get_another_user_by_id_success(user_use_case):
    user_id_needed = "32d8790f-bce9-430e-ad70-b8a410cd66e9"
    user_data = User(role=Role.ADMIN)
    requested_user = await user_use_case.get_another_user_by_id(
        user_id_needed, user_data
    )
    assert requested_user["id"] == user_id_needed


@pytest.mark.asyncio
async def test_edit_another_user_by_id_no_data_error(user_use_case):
    new_user_data = User(name="ekaterina1234")
    user_id_needed = "32d8790f-bce9-430e-ad70-b8a410cd66e1"
    user_data = User(role=Role.USER)
    with pytest.raises(NoDataError) as error:
        await user_use_case.edit_another_user_by_id(
            new_user_data, user_id_needed, user_data
        )
    assert str(error.value.args[0]) == "Could not find user"


@pytest.mark.asyncio
async def test_edit_another_user_by_id_no_permission_error(user_use_case):
    new_user_data = User(name="ekaterina1234")
    user_id_needed = "32d8790f-bce9-430e-ad70-b8a410cd66e9"
    user_data = User(role=Role.USER)
    with pytest.raises(NoPermissionsError) as error:
        await user_use_case.edit_another_user_by_id(
            new_user_data, user_id_needed, user_data
        )
    assert str(error.value.args[0]) == "No permissions"


@pytest.mark.asyncio
async def test_edit_another_user_by_id_success(user_use_case):
    new_user_data = User(name="ekaterina1234")
    user_id_needed = "32d8790f-bce9-430e-ad70-b8a410cd66e9"
    user_data = User(role=Role.ADMIN)
    requested_user = await user_use_case.edit_another_user_by_id(
        new_user_data, user_id_needed, user_data
    )
    assert requested_user["name"] == new_user_data.name
