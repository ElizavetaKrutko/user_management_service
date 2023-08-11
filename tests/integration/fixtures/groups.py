import pytest

from app.adapters.orm_engines.models import GroupORM


# ====== Valid Group 1 ===== #
@pytest.fixture(scope="session")
def group1_in_db_model() -> GroupORM:
    group_in_db = GroupORM()

    group_in_db.id = 1
    group_in_db.name = "test_group1"

    return group_in_db


# ====== Valid Group 2 ===== #
@pytest.fixture(scope="session")
def group2_in_db_model() -> GroupORM:
    group_in_db = GroupORM()

    group_in_db.id = 2
    group_in_db.name = "test_group2"

    return group_in_db
