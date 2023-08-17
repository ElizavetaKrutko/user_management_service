from fastapi import Depends

from app.adapters.orm_engines.sql_alchemy import SQLAlchemy
from app.common.app_settings import BaseAppSettings
from app.common.config import get_settings

# SQLALCHEMY_DATABASE_URL = f"{settings.DB_DIALECT}://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
# SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://postgres:root@postgres:5432/postgres"


class SQLAlchemyDependency:
    def __init__(self):
        self.sqlalchemy = None

    async def __call__(
        self, settings: BaseAppSettings = Depends(get_settings)
    ) -> SQLAlchemy:
        self.sqlalchemy = (
            SQLAlchemy.start(settings.get_db_url)
            if not self.sqlalchemy
            else self.sqlalchemy
        )
        return self.sqlalchemy


get_sql_alchemy = SQLAlchemyDependency()


async def get_db(sqlalchemy: SQLAlchemy = Depends(get_sql_alchemy)):
    async with sqlalchemy.session_maker() as session:
        yield session
