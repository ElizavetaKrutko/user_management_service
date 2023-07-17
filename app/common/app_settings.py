import logging
from enum import Enum
from typing import Any

from pydantic import BaseSettings, Field, SecretStr


class EnvironmentTypes(Enum):
    test: str = "test"
    local: str = "local"
    dev: str = "dev"
    prod: str = "prod"


class BaseAppSettings(BaseSettings):
    environment: EnvironmentTypes = Field(EnvironmentTypes.local, env="API_ENVIRONMENT")
    debug: bool = True
    title: str = "User management service"
    version: str = "0.1.0"
    allowed_hosts: list[str] = ["*"]
    algorithm: str = Field("HS256", env="ALGORITHM")
    jwt_access_secret_key: str = Field("abracadabra", env="JWT_ACCESS_SECRET_KEY")
    jwt_refresh_secret_key: str = Field("avadacedabra", env="JWT_REFRESH_SECRET_KEY")
    db_driver_name: str = "postgresql+asyncpg"
    db_username: str = Field("postgres", env="DB_USERNAME")
    db_host: str = Field("postgres", env="DB_HOST")
    db_password: SecretStr = Field("root", env="DB_PASSWORD")
    db_database: str = Field("postgres", env="DB_NAME")
    db_port: int | None

    @property
    def get_db_creds(self):
        return {
            "drivername": self.db_driver_name,
            "username": self.db_username,
            "host": self.db_host,
            "port": self.db_port,
            "database": self.db_database,
            "password": self.db_password.get_secret_value(),
        }

    @property
    def get_token_creds(self):
        return {
            "jwt_algorithm": self.algorithm,
            "jwt_access_secret_key": self.jwt_access_secret_key,
            "jwt_refresh_secret_key": self.jwt_refresh_secret_key,
        }

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
        }


class TestSettings(BaseAppSettings):
    title: str = "Test environment - User management service"


class LocalSettings(BaseAppSettings):
    title: str = "Local environment - User management service"


class DevelopmentSettings(BaseAppSettings):
    title: str = "Development environment - User management service"
    logging_level: int = logging.DEBUG


class ProductionSettings(BaseAppSettings):
    debug: bool = False
