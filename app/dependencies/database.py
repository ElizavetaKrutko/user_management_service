from fastapi import Depends

from app.adapters.orm_engines.sql_alchemy import SQLAlchemy

# SQLALCHEMY_DATABASE_URL = f"{settings.DB_DIALECT}+asyncpg://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://postgres:root@postgres:5432/postgres"


class SQLAlchemyDependency:
    def __init__(self):
        self.sqlalchemy = None

    async def __call__(self) -> SQLAlchemy:
        self.sqlalchemy = (
            SQLAlchemy.start(SQLALCHEMY_DATABASE_URL)
            if not self.sqlalchemy
            else self.sqlalchemy
        )
        return self.sqlalchemy


get_sql_alchemy = SQLAlchemyDependency()


async def get_db(sqlalchemy: SQLAlchemy = Depends(get_sql_alchemy)):
    async with sqlalchemy.session_maker() as session:
        yield session
