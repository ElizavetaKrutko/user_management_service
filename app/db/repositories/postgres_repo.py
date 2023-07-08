from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Group


class PostgresRepository:
    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.db = db

    async def get_groups(self):
        stmt = select(Group)
        res = await self.db.execute(stmt)

        return res.scalars().all()
