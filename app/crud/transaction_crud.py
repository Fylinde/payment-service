from sqlalchemy.orm import Session
from app.models.transaction_model import TransactionModel
from app.schemas.payment_schema import PaymentDetails
import logging

logger = logging.getLogger(__name__)


def create_transaction(db: Session, payment_details: PaymentDetails, amount: float):
    # Access payment details fields from `payment_details`
    db_transaction = TransactionModel(
        card_token=payment_details.card_number, 
        amount=amount,
        currency="USD"
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction_status(db: Session, transaction_id: int, status: str):
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if transaction:
        transaction.status = status
        db.commit()
        db.refresh(transaction)
    return transaction

def save_payment_token(db: Session, card_token: str, currency: str, token: str, status: str = "unverified", amount: float = None):
    """
    Saves the payment token into the database, ensuring a non-null value for `amount`.
    """
    # If amount is None, set a default value of 0.0 for transactions that do not require it
    if amount is None:
        amount = 0.0

    try:
        logger.debug(f"Saving payment token with values: card_token={card_token}, amount={amount}, currency={currency}, token={token}, status={status}")

        # Create and save the transaction record
        payment_token = TransactionModel(card_token=card_token, amount=amount, currency=currency, token=token, status=status)
        db.add(payment_token)
        db.commit()
        db.refresh(payment_token)

        logger.info(f"Payment token saved successfully with ID {payment_token.id}")
        return payment_token
    except Exception as e:
        logger.error("Error saving payment token", exc_info=True)
        raise e

def delete_payment_token(db: Session, token: str):
    db.query(TransactionModel).filter(TransactionModel.token == token).delete()
    db.commit()
