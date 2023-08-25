from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class SQLAlchemy:
    def __init__(self, session_maker):
        self.session_maker = session_maker

    @staticmethod
    def get_async_engine(database_url: URL) -> AsyncEngine:
        return create_async_engine(database_url, echo=False)

    @classmethod
    def start(cls, database_url: URL):
        engine = cls.get_async_engine(database_url)
        async_session = sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )
        return cls(async_session)
