from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.domain.repositories.email_repository import EmailRepository
from app.domain.services.email_service import EmailService
from app.data.schemas import EmailRequestSchema
from app.utils import standard_response 
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get the email service
def get_email_service(db: Session = Depends(get_db)):
    email_repo = EmailRepository(db)
    return EmailService(email_repo)

@router.post("/send/", status_code=201)
async def send_email(
    email_request: EmailRequestSchema,
    email_service: EmailService = Depends(get_email_service)
):
    try:
        email = await email_service.send_email(email_request)  # Await sending
        return standard_response(
            success=True,
            title="Email Sent Successfully",
            message="The email has been sent.",
            code=201,
            data={"email_id": email.id}
        )
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return standard_response(
            success=False,
            title="Email Sending Failed",
            message=f"Error sending email: {e}",
            code=500,
            data=None
        )
