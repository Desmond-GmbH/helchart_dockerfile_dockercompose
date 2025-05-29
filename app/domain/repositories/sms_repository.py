from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.data.models import SMS, SMSRecipient


class AbstractSMSRepository(ABC):
    @abstractmethod
    def save_sms(self, message: str, recipients: list[str], status: str = "pending"):
        pass


class SMSRepository(AbstractSMSRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_sms(self, message: str, recipients: list[str], status: str = "pending"):
        try:
            # Create SMS record
            sms_record = SMS(message=message, status=status)
            self.db.add(sms_record)
            self.db.flush()

            # Add recipients using the ORM
            for recipient in recipients:
                sms_recipient = SMSRecipient(sms_id=sms_record.id, recipient_number=recipient)
                self.db.add(sms_recipient)

            self.db.commit()
            return sms_record
        except Exception as e:
            self.db.rollback()
            raise e
