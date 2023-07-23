from app.ports.cloud_port import CloudRepositoryPort


class AmazonRepository(CloudRepositoryPort):
    def __init__(self) -> None:
        pass

    def create_reset_password_email_template(self, reset_password_url: str):
        # TODO: add logic of generating reset email
        pass

    async def send_reset_password_email(self, email: str, reset_password_url: str):
        email_template = self.create_reset_password_email_template(reset_password_url)
        await self.send_email(email, email_template)
        return "Please, check your email for reset password url"

    async def send_email(self, email: str, email_template: str):
        # TODO: add bolo3 module with sending email logic
        pass
