import logging

from sqlalchemy import exc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common import utils
from app.db.models import GroupORM, UserORM
from app.rest import schemas


class PostgresRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_user(self, new_user_data: schemas.UserCreate):
        try:
            db_new_user_dict = new_user_data.dict()
            hashed_password = utils.get_hashed_password(db_new_user_dict["password"])
            del db_new_user_dict["password"]
            db_new_user_dict["hashed_password"] = hashed_password

            db_new_user = UserORM(**db_new_user_dict)

            self.db.add(db_new_user)

            await self.db.commit()
            await self.db.refresh(db_new_user)

            logging.info(f"Created new entity: {db_new_user}.")

            return db_new_user

        except exc.IntegrityError as e:
            await self.db.rollback()
            raise e

    async def get_user_by_id(self, user_id):
        db_user = select(UserORM).where(UserORM.id == user_id)
        res = await self.db.execute(db_user)
        logging.error(res)
        return res.scalars().first()

    async def get_user_by_login(self, username, email=None, phone_number=None):
        if email is None:
            email = username
        if phone_number is None:
            phone_number = username
        stmt = select(UserORM).where(
            or_(
                UserORM.username == username,
                UserORM.email == email,
                UserORM.phone_number == phone_number,
            )
        )
        res = await self.db.execute(stmt)

        return res.scalars().first()

    async def get_groups(self):
        stmt = select(GroupORM)
        res = await self.db.execute(stmt)

        return res.scalars().all()
