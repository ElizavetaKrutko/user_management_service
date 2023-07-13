import logging
from os.path import dirname, expanduser, join

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseSettings

# dotenv_path = join(dirname(__file__), "../../envs/.env")
# logging.error(dotenv_path)
load_dotenv(dotenv_path="root:/user_management_service/app/envs/.env")


class Settings(BaseSettings):
    class Config:
        env_file = find_dotenv(".env")
        env_file_encoding = "utf-8"


settings = Settings()
