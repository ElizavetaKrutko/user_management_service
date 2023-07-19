import uuid

from fastapi import HTTPException, status
from sqlalchemy import exc

from app.adapters.orm_engines.models import Role
from app.domain.user import User
from app.ports.redis_port import NoSqlDBRepositoryPort
from app.ports.user_port import UserRepositoryPort
from app.rest.routes import schemas


class UserUseCase:
    def __init__(
        self, db_repo: UserRepositoryPort, no_sql_db_repo: NoSqlDBRepositoryPort
    ):
        self.db_repo = db_repo
        self.no_sql_db_repo = no_sql_db_repo

    async def patch_user(self, new_user_data: User, user_id: uuid.UUID):
        try:
            updated_user = await self.db_repo.update_user_by_id(new_user_data, user_id)
            return schemas.UserPublicInfo.from_orm(updated_user)

        except exc.IntegrityError as err:
            err_msg = str(err.orig).split(":")[-1].replace("\n", "").strip()
            raise HTTPException(status_code=400, detail=err_msg)

    async def delete_user(self, user_id: uuid.UUID):
        try:
            deleted_user_id = await self.db_repo.delete_user(user_id)
            await self.no_sql_db_repo.delete_users_tokens(user_id)
            return deleted_user_id

        except exc.IntegrityError as err:
            err_msg = str(err.orig).split(":")[-1].replace("\n", "").strip()
            raise HTTPException(status_code=400, detail=err_msg)

    async def get_another_user_by_id(
        self, user_id_needed: uuid.UUID, user_data: schemas.UserInfo
    ):
        db_user_needed = await self.db_repo.get_user_by_id(user_id=user_id_needed)

        if db_user_needed is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )

        if (
            user_data.role == Role.ADMIN or user_data.role == Role.MODERATOR
        ) and db_user_needed.group_id == user_data.group_id:
            return schemas.UserInfo.from_orm(db_user_needed)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No permissions",
            )

    async def edit_another_user_by_id(
        self,
        new_user_data: User,
        user_id_needed: uuid.UUID,
        user_data: schemas.UserInfo,
    ):
        db_user_needed = await self.db_repo.get_user_by_id(user_id=user_id_needed)

        if db_user_needed is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )

        if (
            user_data.role == Role.ADMIN
            and db_user_needed.group_id == user_data.group_id
        ):
            try:
                updated_user = await self.db_repo.update_user_by_id(
                    new_user_data, user_id_needed
                )
            except exc.IntegrityError as err:
                err_msg = str(err.orig).split(":")[-1].replace("\n", "").strip()
                raise HTTPException(status_code=400, detail=err_msg)

            return schemas.UserPublicInfo.from_orm(updated_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No permissions",
            )
