from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.data.models import Email, EmailRecipient

class AbstractEmailRepository(ABC):
    @abstractmethod
    def save_email(self, subject: str, body: str, recipients: list[str], status: str = "pending"):
        pass

class EmailRepository(AbstractEmailRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_email(self, subject: str, body: str, recipients: list[str], status: str = "pending"):
        email = Email(subject=subject, body=body, status=status)
        self.db.add(email)
        self.db.commit()
        for recipient in recipients:
            email_recipient = EmailRecipient(email_id=email.id, recipient_email=recipient)
            self.db.add(email_recipient)
        self.db.commit()
        return email
