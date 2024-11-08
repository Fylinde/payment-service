from app.utils.token_utils import generate_payment_token
from app.crud.transaction_crud import create_transaction, update_transaction_status
from sqlalchemy.orm import Session

def process_payment(db: Session, payment_details, amount: float, currency: str):
    # Generate a mock token for the card
    card_token = generate_payment_token()

    # Create a new transaction in the database with pending status
    transaction = create_transaction(db, card_token, amount, currency)

    # Simulate processing logic
    # Set the status to "completed" or "failed" based on some criteria
    transaction_status = "completed" if amount > 0 else "failed"
    update_transaction_status(db, transaction.id, transaction_status)

    return transaction
