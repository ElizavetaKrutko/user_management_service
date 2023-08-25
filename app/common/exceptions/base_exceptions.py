from abc import ABC, abstractmethod


class BaseDBError(Exception):
    pass


class BaseORMError(Exception):
    @abstractmethod
    def bad_request_error(self) -> Exception:
        pass


class BaseBadRequestError(Exception):
    pass


class BaseInvalidTokenError(Exception):
    pass


class BaseNoPermissionsError(Exception):
    pass


class BaseNoDataError(Exception):
    pass


class BaseAppExceptions(ABC):
    @abstractmethod
    def db_error(self, message: str) -> BaseDBError:
        pass

    @abstractmethod
    def orm_error(self, error: Exception) -> BaseORMError:
        pass

    @abstractmethod
    def bad_request_error(
        self, message: str, headers: dict = None
    ) -> BaseBadRequestError:
        pass

    @abstractmethod
    def invalid_token_error(
        self, message: str, headers: dict = None
    ) -> BaseInvalidTokenError:
        pass

    @abstractmethod
    def no_permissions_error(
        self, message: str, headers: dict = None
    ) -> BaseNoPermissionsError:
        pass

    @abstractmethod
    def no_data_error(self, message: str, headers: dict = None) -> BaseNoDataError:
        pass
