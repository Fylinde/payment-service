import hashlib
import uuid
from app.schemas.payment_schema import TokenizationRequest
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generate_card_token(payment_details: TokenizationRequest) -> str:
    try:
        # Log the received card number (masking most of it for security)
        logger.debug(f"Generating token for card number ending in {payment_details.cardNumber[-4:]}")

        # Step 1: Generate a unique identifier
        unique_id = uuid.uuid4().hex
        logger.debug(f"Generated unique ID: {unique_id}")

        # Step 2: Hash the card number
        try:
            card_hash = hashlib.sha256(payment_details.cardNumber.encode()).hexdigest()
            logger.debug(f"Generated card hash (first 10 characters): {card_hash[:10]}")
        except Exception as hash_error:
            logger.error("Error hashing card number", exc_info=True)
            raise hash_error

        # Step 3: Combine unique ID and card hash to create token
        token = f"{unique_id}-{card_hash[:10]}"
        logger.debug(f"Generated token: {token}")

        return token
    except Exception as e:
        # Use logger.exception to log with full traceback, avoiding "unused" warning
        logger.exception("Failed to generate token")
        raise e  # Explicitly re-raise the exception
