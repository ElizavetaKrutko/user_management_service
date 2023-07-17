import logging

from sqlalchemy import exc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.orm_engines.models import UserORM
from app.common import utils
from app.domain.user import User
from app.ports.user_port import UserRepositoryPort


# inherit from postgresPort, add domains, not SQLAlchemy objects
class SQLAlchemyUserRepository(UserRepositoryPort):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_user(self, new_user_data: User):
        try:
            hashed_password = utils.get_hashed_password(new_user_data.password)
            del new_user_data.password
            new_user_data.hashed_password = hashed_password

            db_new_user = await self.__create_orm_user(new_user_data)

            logging.info(f"Created new entity: {db_new_user}.")

            return db_new_user

        except exc.IntegrityError as e:
            await self.db.rollback()
            raise e

    async def __create_orm_user(self, new_user_data):
        db_new_user = UserORM()

        self.db.add(db_new_user)

        db_new_user.name = new_user_data.name
        db_new_user.surname = new_user_data.surname
        db_new_user.username = new_user_data.username
        db_new_user.hashed_password = new_user_data.hashed_password
        db_new_user.phone_number = new_user_data.phone_number
        db_new_user.email = new_user_data.email
        db_new_user.role = new_user_data.role
        db_new_user.image_path = new_user_data.image_path
        db_new_user.is_blocked = new_user_data.is_blocked
        db_new_user.group_id = new_user_data.group_id

        await self.db.commit()
        await self.db.refresh(db_new_user)

        return db_new_user

    async def get_user_by_id(self, user_id):
        db_user = select(UserORM).where(UserORM.id == user_id)
        res = await self.db.execute(db_user)
        logging.debug(res)
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
