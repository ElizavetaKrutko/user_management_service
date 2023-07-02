from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from app.common.config import settings

# SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://postgres:root@localhost:5432/postgres'
SQLALCHEMY_DATABASE_URL = f"{settings.DB_DIALECT}+asyncpg://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()
