from twilio.rest import Client
from app.config import config
from app.domain.repositories.sms_repository import AbstractSMSRepository
from app.data.schemas import SMSRequestSchema


class SMSService:
    def __init__(self, sms_repo: AbstractSMSRepository):
        self.sms_repo = sms_repo
        self.twilio_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

    def send_sms(self, sms_request: SMSRequestSchema):
        # Save SMS to the database
        sms_record = self.sms_repo.save_sms(
            message=sms_request.message,
            recipients=sms_request.recipients,
        )

        # Send SMS to all recipients
        for recipient in sms_request.recipients:
            try:
                message = self.twilio_client.messages.create(
                    body=sms_request.message,
                    from_=config.TWILIO_PHONE_NUMBER,
                    to=recipient
                )
                # Log message SID (unique identifier for each Twilio message)
                print(f"Message sent to {recipient} with SID: {message.sid}")
            except Exception as e:
                print(f"Failed to send SMS to {recipient}: {e}")
                # Optionally update the SMS status to failed
                sms_record.status = "failed"
                self.sms_repo.db.commit()
                raise e

        # Update status to "sent" if all succeed
        sms_record.status = "sent"
        self.sms_repo.db.commit()

        return sms_record
