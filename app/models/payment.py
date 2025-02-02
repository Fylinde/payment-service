from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import BaseModel

class PaymentDetailsModel(BaseModel):
    __tablename__ = "payment_details"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, nullable=False)
    cardholder_name = Column(String, nullable=False)
    expiry_month = Column(Integer, nullable=False)
    expiry_year = Column(Integer, nullable=False)
    cvv = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False)
    verification_status = Column(String, default="unverified")  # Default to unverified
    status = Column(String, default="unverified", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
