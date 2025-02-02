from app.utils.token_utils import generate_card_token, generate_unique_token
from app.crud.transaction_crud import create_transaction, update_transaction_status, save_payment_token
from sqlalchemy.orm import Session
from app.schemas.payment_schema import TokenizationRequest, PaymentTokenResponse
import logging
from fastapi import HTTPException
logger = logging.getLogger(__name__)


def process_payment(db: Session, payment_details, amount: float, currency: str):
    # Generate a mock token for the card
    card_token = generate_card_token()

    # Create a new transaction in the database with pending status
    transaction = create_transaction(db, card_token, amount, currency)

    # Simulate processing logic
    # Set the status to "completed" or "failed" based on some criteria
    transaction_status = "completed" if amount > 0 else "failed"
    update_transaction_status(db, transaction.id, transaction_status)

    return transaction

def tokenize_payment_details(db: Session, payment_details: TokenizationRequest) -> PaymentTokenResponse:
    try:
        # Log incoming details (excluding sensitive data for security)
        logger.debug(f"Starting tokenization for: {payment_details.cardholderName}")

        # Tokenize card details
        card_token = generate_card_token(payment_details)
        logger.debug(f"Generated card token: {card_token}")
        logger.debug(f"Tokenization request details: {payment_details}")
        #logger.debug(f"Generated token: {response.token}")


        # Generate a unique token for this request
        unique_token = generate_unique_token(card_token)
        logger.debug(f"Generated unique transaction token: {unique_token}")

        # Save tokenized details in the database
        saved_token = save_payment_token(
            db=db,
            card_token=card_token,
            amount=None,  # Not tied to any payment
            currency=payment_details.currency,
            token=unique_token,
            status="unverified"  # Mark as unverified for registration
        )

        logger.info(f"Saved token with status 'unverified': {saved_token.token}")

        # Return the token and status
        return PaymentTokenResponse(
            token=saved_token.token,
            status="success",
            message="Card tokenized successfully"
        )

    except Exception as e:
        logger.error("Error during tokenization", exc_info=True)
        raise HTTPException(status_code=500, detail="Tokenization failed")
