import uuid

from app.adapters.orm_engines.models import Role
from app.common.exceptions.base_exceptions import BaseAppExceptions
from app.domain.user import User
from app.ports.redis_port import NoSqlDBRepositoryPort
from app.ports.user_port import UserRepositoryPort
from app.rest.routes import schemas
from app.rest.routes.filters import UsersFilter


class UserUseCase:
    def __init__(
        self,
        db_repo: UserRepositoryPort,
        no_sql_db_repo: NoSqlDBRepositoryPort,
        app_exceptions: BaseAppExceptions,
    ):
        self.db_repo = db_repo
        self.no_sql_db_repo = no_sql_db_repo
        self.app_exceptions = app_exceptions

    async def patch_user(self, new_user_data: User, user_id: uuid.UUID):
        return await self.db_repo.update_user_by_id(new_user_data, user_id)

    async def delete_user(self, user_id: uuid.UUID):
        deleted_user_id = await self.db_repo.delete_user(user_id)
        await self.no_sql_db_repo.delete_users_tokens(user_id)
        return deleted_user_id

    async def get_another_user_by_id(self, user_id_needed: uuid.UUID, user_data: User):
        db_user_needed = await self.db_repo.get_user_by_id(user_id=user_id_needed)

        if db_user_needed is None:
            raise self.app_exceptions.no_data_error(message="Could not find user")

        if user_data.role.value == Role.ADMIN.value or (
            user_data.role == Role.MODERATOR
            and db_user_needed.group_id == user_data.group_id
        ):
            return db_user_needed
        else:
            raise self.app_exceptions.no_permissions_error(message="No permissions")

    async def edit_another_user_by_id(
        self,
        new_user_data: User,
        user_id_needed: uuid.UUID,
        user_data: User,
    ):
        db_user_needed = await self.db_repo.get_user_by_id(user_id=user_id_needed)

        if db_user_needed is None:
            raise self.app_exceptions.no_data_error(message="Could not find user")

        if user_data.role.value == Role.ADMIN.value:
            updated_user = await self.db_repo.update_user_by_id(
                new_user_data, user_id_needed
            )
            return updated_user
        else:
            raise self.app_exceptions.no_permissions_error(message="No permissions")

    async def get_users_with_queries(
        self, user_data: schemas.UserInfo, users_filter: UsersFilter
    ):
        if user_data.role.value == Role.ADMIN.value:
            return await self.db_repo.get_users_by_filters(users_filter)
        elif user_data.role == Role.MODERATOR:
            return await self.db_repo.get_users_by_filters(
                users_filter, user_data.group_id
            )
        else:
            raise self.app_exceptions.no_permissions_error(message="No permissions")
