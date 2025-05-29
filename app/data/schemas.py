from pydantic import BaseModel, EmailStr, validator 
from typing import List
import re 


class EmailRequestSchema(BaseModel):
    recipients: List[EmailStr]
    subject: str
    body: str


class SMSRequestSchema(BaseModel):
    recipients: List[str]
    message: str

    @validator("recipients", each_item=True)
    def validate_recipient(cls, recipient):
        pattern = r"^\+?[1-9]\d{1,14}$"
        if not re.match(pattern, recipient):
            raise ValueError(f"Invalid phone number format: {recipient}. Ensure it follows E.164 format.")
        return recipient
