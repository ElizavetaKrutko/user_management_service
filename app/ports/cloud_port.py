from abc import ABC, abstractmethod


class CloudRepositoryPort(ABC):
    @abstractmethod
    async def create_reset_password_email_template(self, reset_password_url: str):
        pass

    @abstractmethod
    async def send_reset_password_email(self, email: str, reset_password_url: str):
        pass

    @abstractmethod
    async def send_email(self, email: str, email_template: str):
        pass
