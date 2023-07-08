from os.path import dirname, join

from dotenv import load_dotenv
from pydantic import BaseSettings

dotenv_path = join(dirname(__file__), "../../envs/.env")
load_dotenv(dotenv_path=dotenv_path)


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
