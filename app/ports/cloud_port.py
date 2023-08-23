from abc import ABC, abstractmethod


class CloudRepositoryPort(ABC):
    @abstractmethod
    async def send_reset_password_email(self, email: str, reset_password_url: str):
        pass

    @abstractmethod
    async def send_email(self, email: str, reset_password_url: str):
        pass
