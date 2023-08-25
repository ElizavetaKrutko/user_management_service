from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.common.exceptions.base_exceptions import (
    BaseAppExceptions,
    BaseBadRequestError,
    BaseDBError,
    BaseInvalidTokenError,
    BaseNoDataError,
    BaseNoPermissionsError,
    BaseORMError,
)


class DBError(BaseDBError):
    pass


class ORMError(BaseORMError):
    def __init__(self, error: IntegrityError):
        self.error = error

    def __convert__(self) -> str:
        return str(self.error.orig).split(":")[-1].replace("\n", "").strip()

    def bad_request_error(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=self.__convert__()
        )


class BadRequestError(BaseBadRequestError, HTTPException):
    def __init__(self, message: str, headers: dict):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = message
        self.headers = headers


class InvalidTokenError(BaseInvalidTokenError, HTTPException):
    def __init__(self, message: str, headers: dict):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = message
        self.headers = headers


class NoPermissionsError(BaseNoPermissionsError, HTTPException):
    def __init__(self, message: str, headers: dict):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = message
        self.headers = headers


class NoDataError(BaseNoDataError, HTTPException):
    def __init__(self, message: str, headers: dict):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = message
        self.headers = headers


class AppExceptions(BaseAppExceptions):
    def db_error(self, message) -> DBError:
        return DBError(message)

    def orm_error(self, error: IntegrityError) -> ORMError:
        return ORMError(error)

    def bad_request_error(self, message: str, headers: dict = None) -> BadRequestError:
        return BadRequestError(message, headers)

    def invalid_token_error(
        self, message: str, headers: dict = None
    ) -> InvalidTokenError:
        return InvalidTokenError(message, headers)

    def no_permissions_error(
        self, message: str, headers: dict = None
    ) -> NoPermissionsError:
        return NoPermissionsError(message, headers)

    def no_data_error(self, message: str, headers: dict = None) -> NoDataError:
        return NoDataError(message, headers)
