"""Connection to the Postgres database."""
import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.common.config import settings

# SQLALCHEMY_DATABASE_URL = f"{settings.DB_DIALECT}+asyncpg://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://postgres:root@postgres:5432/postgres"


def get_async_engine() -> AsyncEngine:
    try:
        async_engine: AsyncEngine = create_async_engine(
            SQLALCHEMY_DATABASE_URL,
            future=True,
        )
    except SQLAlchemyError as e:
        logging.warning("Unable to establish db engine, database might not exist yet")
        logging.warning(e)

    return async_engine
