from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.domain.repositories.sms_repository import SMSRepository
from app.domain.services.sms_service import SMSService
from app.data.schemas import SMSRequestSchema
from app.utils import standard_response

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_sms_service(db: Session = Depends(get_db)):
    sms_repo = SMSRepository(db)
    return SMSService(sms_repo)

@router.post("/send/", status_code=201)
async def send_sms(
        sms_request: SMSRequestSchema,
        sms_service: SMSService = Depends(get_sms_service)
):
    try:
        sms = sms_service.send_sms(sms_request)
        return standard_response(
            success=True,
            title="SMS Sent Successfully",
            message="The SMS has been sent.",
            code=201,
            data={"sms_id": sms.id}
        )
    except Exception as e:
        return standard_response(
            success=False,
            title="SMS Sending Failed",
            message=f"Error sending SMS: {e}",
            code=500,
            data=None
        )
