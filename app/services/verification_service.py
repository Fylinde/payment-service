import requests
import logging
from app.config import settings

AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL  # Base URL for auth-service

def send_verification_request(to_contact: str, seller_type: str, is_email: bool = True):
    """
    Sends a verification request to the auth-service to send an email or SMS to the seller.
    
    Args:
        to_contact (str): Email address or phone number of the seller.
        seller_type (str): Type of seller - "professional" or "individual".
        is_email (bool): Flag to indicate if contact is an email (True) or phone number (False).
    
    Returns:
        bool: True if the verification request was sent successfully, False otherwise.
    """
    verification_url = f"{AUTH_SERVICE_URL}/send-verification"
    payload = {
        "contact": to_contact,
        "is_email": is_email,
        "seller_type": seller_type,  # Indicate the seller type
    }

    try:
        response = requests.post(verification_url, json=payload)
        response.raise_for_status()
        logging.info(f"Verification request sent successfully to {seller_type} seller at {to_contact}")
        return True
    except requests.HTTPError as e:
        logging.error(f"Failed to send verification request to {to_contact} for {seller_type} seller: {e}")
        return False
