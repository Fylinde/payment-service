from fastapi import APIRouter, HTTPException, Request, Depends
from app.schemas.payment_schema import TokenizationRequest, PaymentTokenResponse
from app.services.payment_service import tokenize_payment_details
import logging
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.transaction_model import TransactionModel

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/tokenize-card", response_model=PaymentTokenResponse)
async def tokenize_card(payment_details: TokenizationRequest, request: Request, db: Session = Depends(get_db)):
    logger.debug(f"Received payment details: {payment_details.dict()}")

    try:
        # Log the request headers and body for verification
        logger.debug(f"Request headers: {request.headers}")
        logger.debug(f"Received payment details: {payment_details}")

        # Extract expiry month and year from nested expiryDate for further processing, if needed
        expiry_month = payment_details.expiryDate.month
        expiry_year = payment_details.expiryDate.year
        logger.debug(f"Expiry Month: {expiry_month}, Expiry Year: {expiry_year}")

        # Tokenize the card and save to the database
        response = tokenize_payment_details(db, payment_details)

        # Log the generated token response
        logger.debug(f"Generated token response: {response}")
        return response
    except Exception as e:
        # Log detailed error information
        logger.error(f"Error during tokenization: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Payment tokenization failed")

@router.post("/verify-payment/{token}")
def verify_payment(token: str, db: Session = Depends(get_db)):
    try:
        payment_record = db.query(TransactionModel).filter(TransactionModel.token == token).first()

        if not payment_record:
            raise HTTPException(status_code=404, detail="Token not found")

        payment_record.status = "verified"
        db.commit()
        db.refresh(payment_record)

        logger.info(f"Payment token {token} marked as verified")
        return {"message": "Payment verified successfully"}
    except Exception as e:
        logger.error("Error verifying payment", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to verify payment")
