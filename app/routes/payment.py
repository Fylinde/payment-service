from fastapi import APIRouter, HTTPException,Request
from app.schemas.payment_schema import TokenizationRequest, PaymentTokenResponse
from app.utils.token_utils import generate_card_token
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


router = APIRouter()

@router.post("/tokenize-card", response_model=PaymentTokenResponse)
async def tokenize_card(payment_details: TokenizationRequest, request: Request):
    try:
        # Log the request headers and body for verification
        logger.debug(f"Request headers: {request.headers}")
        logger.debug(f"Received payment details: {payment_details}")

        # Generate a token for the card details
        token = generate_card_token(payment_details)
        response = {"token": token}

        # Log the generated token
        logger.debug(f"Generated token: {response}")
        return response
    except Exception as e:
        # Log detailed error information
        logger.error(f"Error during tokenization: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Payment tokenization failed")