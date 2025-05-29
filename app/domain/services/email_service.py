from app.data.schemas import EmailRequestSchema
from app.domain.repositories.email_repository import AbstractEmailRepository
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import config

conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_FROM,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_STARTTLS=config.MAIL_STARTTLS,
    MAIL_SSL_TLS=config.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
)


class EmailService:
    def __init__(self, email_repo: AbstractEmailRepository):
        self.email_repo = email_repo
        self.mail_client = FastMail(conf)

    async def send_email(self, email_request: EmailRequestSchema):
        # Save the email in the database first
        email = self.email_repo.save_email(
            subject=email_request.subject,
            body=email_request.body,
            recipients=email_request.recipients,
        )

        # Prepare the email
        message = MessageSchema(
            subject=email_request.subject,
            recipients=email_request.recipients,
            body=email_request.body,
            subtype="html",
        )

        try:
            # Send the email
            await self.mail_client.send_message(message)
            email.status = "sent"
        except Exception as e:
            email.status = "failed"
            raise e
        finally:
            # Commit status change
            self.email_repo.db.commit()

        return email
