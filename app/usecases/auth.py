from app.common.config import logger
import uuid
from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy import exc

from app.common import utils
from app.common.config import settings
from app.domain.user import User
from app.ports.redis_port import NoSqlDBRepositoryPort
from app.ports.user_port import UserRepositoryPort
from app.rest.routes import schemas

ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7


class AuthManagementUseCase:
    def __init__(
        self, db_repo: UserRepositoryPort, no_sql_db_repo: NoSqlDBRepositoryPort
    ):
        self.db_repo = db_repo
        self.no_sql_db_repo = no_sql_db_repo

    async def create_jwt_token(self, subject: Union[str, Any]):
        jwt_uuid = uuid.uuid4()
        await self.no_sql_db_repo.activate_jwt(subject, jwt_uuid)
        return {
            "access_token": self.create_access_token(subject, jwt_uuid),
            "refresh_token": self.create_refresh_token(subject, jwt_uuid),
        }

    def create_access_token(self, subject: Union[str, Any], jwt_uuid: uuid.UUID) -> str:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode = {
            "exp": expires_delta,
            "sub": str(subject),
            "jwt_uuid": str(jwt_uuid),
        }
        logger.debug(settings.jwt_access_secret_key)
        logger.debug(settings.algorithm)
        encoded_jwt = jwt.encode(
            to_encode, settings.jwt_access_secret_key, settings.algorithm
        )

        return encoded_jwt

    def create_refresh_token(
        self, subject: Union[str, Any], jwt_uuid: uuid.UUID
    ) -> str:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

        to_encode = {
            "exp": expires_delta,
            "sub": str(subject),
            "jwt_uuid": str(jwt_uuid),
        }
        encoded_jwt = jwt.encode(
            to_encode, settings.jwt_refresh_secret_key, settings.algorithm
        )
        return encoded_jwt

    async def create_user(self, new_user_data: User):
        try:
            duplicate_user = await self.db_repo.get_user_by_login(
                new_user_data.username, new_user_data.email, new_user_data.phone_number
            )
            if duplicate_user:
                error_message = ""
                if duplicate_user.username == new_user_data.username:
                    error_message = "User with provided user name already exists!"
                elif duplicate_user.email == new_user_data.email:
                    error_message = "User with provided email already exists!"
                elif duplicate_user.phone_number == new_user_data.phone_number:
                    error_message = "User with provided phone number already exists!"
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=error_message
                )
            else:
                created_user = await self.db_repo.create_user(new_user_data)

                return await self.create_jwt_token(created_user.id)
        except exc.IntegrityError as err:
            err_msg = str(err.orig).split(":")[-1].replace("\n", "").strip()
            raise HTTPException(status_code=400, detail=err_msg)

    async def login_user(self, new_user_data: schemas.UserLogin):
        current_user = await self.db_repo.get_user_by_login(new_user_data.login)
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect login"
            )

        if not utils.verify_password(
            new_user_data.password, current_user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
            )
        return await self.create_jwt_token(current_user.id)

    async def logout_user(self, subject: uuid.UUID):
        await self.no_sql_db_repo.blacklist_jwt(subject)
        return "The user logged out"
