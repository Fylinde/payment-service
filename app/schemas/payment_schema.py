from pydantic import BaseModel, Field, validator
from app.utils.constants import SUPPORTED_CURRENCIES

class ExpiryDate(BaseModel):
    month: str = Field(..., pattern=r"^(0[1-9]|1[0-2])$", description="Expiry month in MM format")
    year: str = Field(..., pattern=r"^\d{2}$", description="Expiry year in YY format")

class PaymentDetails(BaseModel):
    cardNumber: str = Field(..., min_length=13, max_length=19, pattern=r"^\d{13,19}$", description="Card number, 13-19 digits")
    expiryDate: ExpiryDate  # Use ExpiryDate as a nested object
    currency: str = Field(..., max_length=3, description="Currency code, e.g., USD")
    cardholderName: str = Field(..., min_length=1, max_length=50, description="Name on the card")

    class Config:
        schema_extra = {
            "example": {
                "cardNumber": "4111111111111111",
                "expiryDate": {"month": "12", "year": "24"},
                "currency": "USD",
                "cardholderName": "John Doe",
            }
        }

    @validator('currency')
    def validate_currency(cls, v):
        if v not in SUPPORTED_CURRENCIES:
            raise ValueError(f"Currency '{v}' is not supported.")
        return v

class PaymentTokenResponse(BaseModel):
    token: str
    status: str
    message: str
    verification_status: str
    
class TokenizationRequest(BaseModel):
    cardNumber: str = Field(..., min_length=13, max_length=19, pattern=r"^\d{13,19}$", description="Card number, 13-19 digits")
    expiryDate: ExpiryDate
    cardholderName: str = Field(..., min_length=1, max_length=50, description="Name on the card")
    cvv: str = Field(..., min_length=3, max_length=4, description="CVV code, 3-4 digits")
    currency: str = Field(..., max_length=3, description="Currency code, e.g., USD")
    verification_status: str = "unverified"
  
    @validator('currency')
    def validate_currency(cls, v):
        if v not in SUPPORTED_CURRENCIES:
            raise ValueError(f"Currency '{v}' is not supported.")
        return v