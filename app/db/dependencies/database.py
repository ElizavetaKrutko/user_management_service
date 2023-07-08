import logging
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.db_session import get_async_engine


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async session.

    All conversations with the database are established via the session
    objects. Also. the sessions act as holding zone for ORM-mapped objects.
    """
    async_session = sessionmaker(
        bind=get_async_engine(),
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
    async with async_session() as async_sess:
        try:
            yield async_sess

        except SQLAlchemyError as e:
            logging.error("Unable to yield session in database dependency")
            logging.error(e)
