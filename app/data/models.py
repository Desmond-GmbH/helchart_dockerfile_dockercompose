from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String, default="pending")  # e.g., "pending", "sent", "failed"
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Define a relationship to store multiple recipients for each email
    recipients = relationship("EmailRecipient", back_populates="email", cascade="all, delete-orphan")


class EmailRecipient(Base):
    __tablename__ = "email_recipients"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id", ondelete="CASCADE"))
    recipient_email = Column(String, nullable=False)
    email = relationship("Email", back_populates="recipients")


class SMS(Base):
    __tablename__ = "sms_messages"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    status = Column(String, default="pending")  # e.g., "pending", "sent", "failed"
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Define a relationship to store multiple recipients for each SMS
    recipients = relationship("SMSRecipient", back_populates="sms", cascade="all, delete-orphan")

class SMSRecipient(Base):
    __tablename__ = "sms_recipients"

    id = Column(Integer, primary_key=True, index=True)
    sms_id = Column(Integer, ForeignKey("sms_messages.id", ondelete="CASCADE"))
    recipient_number = Column(String, nullable=False)
    sms = relationship("SMS", back_populates="recipients")
