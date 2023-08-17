import boto3

from app.common.config import settings
from app.ports.cloud_port import CloudRepositoryPort


class AmazonRepository(CloudRepositoryPort):
    def __init__(self) -> None:
        self.ses_client = boto3.client(
            "ses",
            region_name=settings.region_name,
            aws_access_key_id=settings.aws_access_key_string,
            aws_secret_access_key=settings.aws_secret_key_string,
        )

    async def send_reset_password_email(self, email: str, reset_password_url: str):
        await self.send_email(email, reset_password_url)
        return "Please, check your email for reset password url"

    async def send_email(self, email: str, reset_password_url: str):
        email_text = (
            f"Hello, press the link {reset_password_url} to reset your password"
        )

        # Send an email using the template
        response = self.ses_client.send_email(
            Source="elizaveta.krutsko@innowise-group.com",
            Destination={"ToAddresses": [email]},
            Message={
                "Subject": {"Data": "Password Reset"},
                "Body": {"Text": {"Data": email_text}},
            },
        )
