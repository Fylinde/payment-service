from pydantic import BaseModel, Field, validator
from app.utils.constants import SUPPORTED_CURRENCIES

class PaymentDetails(BaseModel):
    cardNumber: str = Field(..., min_length=13, max_length=19, pattern=r"^\d{13,19}$", description="Card number, 13-19 digits")
    expiryMonth: str = Field(..., pattern=r"^(0[1-9]|1[0-2])$", description="Expiry month in MM format")
    expiryYear: str = Field(..., pattern=r"^\d{2}$", description="Expiry year in YY format")
    currency: str = Field(..., max_length=3, description="Currency code, e.g., USD")
    cardholderName: str = Field(..., min_length=1, max_length=50, description="Name on the card")

    class Config:
        schema_extra = {
            "example": {
                "cardNumber": "4111111111111111",
                "expiryMonth": "12",
                "expiryYear": "24",
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

class TokenizationRequest(BaseModel):
    cardNumber: str = Field(..., min_length=13, max_length=19, pattern=r"^\d{13,19}$", description="Card number, 13-19 digits")
    expiryMonth: str = Field(..., pattern=r"^(0[1-9]|1[0-2])$", description="Expiry month in MM format")
    expiryYear: str = Field(..., pattern=r"^\d{2}$", description="Expiry year in YY format")
    cardholderName: str = Field(..., min_length=1, max_length=50, description="Name on the card")

