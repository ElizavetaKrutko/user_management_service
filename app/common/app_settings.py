import logging
from enum import Enum
from typing import Any

from pydantic import BaseSettings, Field, SecretStr
from sqlalchemy import URL

from app.common.custom_logging import CustomFormatter


class EnvironmentTypes(Enum):
    test: str = "test"
    local: str = "local"
    dev: str = "dev"
    prod: str = "prod"


class BaseAppSettings(BaseSettings):
    environment: EnvironmentTypes = Field(EnvironmentTypes.local, env="API_ENVIRONMENT")
    debug: bool = Field(True, env="DEBUG_MODE")
    title: str = "User management service"
    version: str = "0.1.0"
    allowed_hosts: list[str] = ["*"]
    app_url: str = Field("https://myapp.com", env="APP_URL")
    algorithm: str = Field("HS256", env="ALGORITHM")
    jwt_access_secret_key: str = Field("abracadabra", env="JWT_ACCESS_SECRET_KEY")
    jwt_refresh_secret_key: str = Field("avadacedabra", env="JWT_REFRESH_SECRET_KEY")
    jwt_reset_password_secret_key: str = Field(
        "abracadabraLALA", env="JWT_RESET_PASSWORD_SECRET_KEY"
    )
    aws_access_key_string: str = Field(
        "AKIAWNR4ADEACKWYFJ4I", env="AWS_ACCESS_KEY_STRING"
    )
    aws_secret_key_string: str = Field(
        "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", env="AWS_SECRET_KEY_STRING"
    )
    region_name: str = Field("us-east-1", env="REGION_NAME")
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
    def get_db_url(self):
        return URL.create(**self.get_db_creds)

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

    def get_logger(self) -> logging.Logger:
        return logging.getLogger(__name__)

    def configure_logging(self) -> None:
        log_lever = (logging.INFO, logging.DEBUG)[self.debug]
        logger = self.get_logger()
        logger.setLevel(log_lever)
        # Define format for logs
        fmt = "%(asctime)s | %(levelname)8s | %(message)s"
        """Configure and format logging used in app."""
        # logging.basicConfig()
        # logging.getLogger('sqlalchemy.engine').setLevel(log_lever)
        # Create stdout handler for logging to the console (logs all five levels)
        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(log_lever)
        stdout_handler.setFormatter(CustomFormatter(fmt))

        logger.addHandler(stdout_handler)


class TestSettings(BaseAppSettings):
    title: str = "Test environment - User management service"


class LocalSettings(BaseAppSettings):
    title: str = "Local environment - User management service"


class DevelopmentSettings(BaseAppSettings):
    title: str = "Development environment - User management service"
    logging_level: int = logging.DEBUG


class ProductionSettings(BaseAppSettings):
    debug: bool = False
