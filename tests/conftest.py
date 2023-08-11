from glob import glob
from typing import Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.orm_engines.sql_alchemy import SQLAlchemy
from app.common.config import logger, settings
from app.dependencies.database import get_db
from app.main import app

pytest.access_token = ""
pytest.refresh_token = ""


# allow fixtures that are in \tests\fixtures folder to be included in conftest
def refactor(string: str) -> str:
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


pytest_plugins = [
    refactor(fixture)
    for fixture in glob("tests/integration/fixtures/*.py")
    if "__" not in fixture
]


# make "trio" warnings go away
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# ===== SQLAlchemy Setup ===== #
@pytest.fixture(scope="session")
async def session():
    """SqlAlchemy testing suite.
    Using ORM while rolling back changes after commit to have independant test cases.
    Implementation of "Joining a Session into an External Transaction (such as for test suite)"
    """
    async_engine = SQLAlchemy.get_async_engine(settings.get_db_url)

    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()

        async_session = AsyncSession(conn, expire_on_commit=False)

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                conn.sync_connection.begin_nested()

        yield async_session

        await async_session.close()
        await conn.rollback()


# ===== FastAPI Setup ===== #
@pytest.fixture()
async def test_app(session) -> FastAPI:
    """Injecting test database as dependancy in app for tests."""

    async def test_get_database() -> Generator:
        yield session

    app.dependency_overrides[get_db] = test_get_database

    return app


@pytest.fixture
async def async_test_client(test_app: FastAPI) -> AsyncClient:
    """Test client that will be used to make requests against our endpoints."""

    # asgi-lifespan - allows testing async applications without having to spin up an ASGI server
    async with LifespanManager(test_app):
        async with AsyncClient(app=test_app, base_url="http://testserver") as ac:
            try:
                yield ac

            except SQLAlchemyError as e:
                logger.error("Error while yielding test client")
