from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import BaseModel

class TransactionModel(BaseModel):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    card_token = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    token = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="unverified", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
