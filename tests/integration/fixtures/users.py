import uuid

import pytest
from fastapi.encoders import jsonable_encoder

from app.adapters.orm_engines.models import UserORM
from app.common.utils import get_hashed_password
from app.rest.routes.schemas import UserCreate


# ====== Valid User 1 ===== #
@pytest.fixture(scope="session")
def user1_in_db_model() -> UserORM:
    db_new_user = UserORM()

    db_new_user.id = uuid.UUID("1b417945-c927-439b-a3bd-8200847e2ef5")
    db_new_user.username = "test_user1"
    db_new_user.hashed_password = get_hashed_password("test_user1_password")
    db_new_user.phone_number = "test_user1_phone"
    db_new_user.email = "test_user1_email"
    db_new_user.group_id = 1
    db_new_user.role = "MODERATOR"
    return db_new_user


# ====== Valid User 2 ===== #
@pytest.fixture(scope="session")
def user2_in_db_model() -> UserORM:
    db_new_user = UserORM()

    db_new_user.id = uuid.UUID("4a5f9ad4-632d-4b9a-971d-e35a800673a8")
    db_new_user.username = "test_user2"
    db_new_user.hashed_password = get_hashed_password("test_user2_password")
    db_new_user.phone_number = "test_user2_phone"
    db_new_user.email = "test_user2_email"
    db_new_user.group_id = 1
    db_new_user.role = "ADMIN"
    return db_new_user


# ====== Valid User 3 ===== #
@pytest.fixture
def user3_create() -> UserCreate:
    """Returns a json compatible dict of example UserCreate model"""
    user = UserCreate(
        username="test_user3",
        password="test_user3_password",
        phone_number="test_user3_phone",
        email="test_user3_email",
        group_id=2,
    )
    return jsonable_encoder(user)


@pytest.fixture
def user3_in_db_schema():
    """Returns a json compatible dict of example UserInDB model"""
    user = UserCreate(
        id=uuid.uuid4(),
        username="test_user3",
        password="test_user3_password",
        phone_number="test_user3_phone",
        email="test_user3_email",
        group_id=2,
    )
    return jsonable_encoder(user.to_entity().dict())


@pytest.fixture
def user3_in_db_model(user3_in_db_schema) -> UserORM:
    return UserORM(**user3_in_db_schema)
