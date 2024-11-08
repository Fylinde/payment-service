from sqlalchemy.orm import Session
from app.models.transaction_model import TransactionModel
from app.schemas.payment_schema import PaymentDetails


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
