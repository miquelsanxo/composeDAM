from utils.db import db
from models.payment import Payment
from utils.exceptions import ModelNotFoundException

def get_all_payments() -> list:
    return Payment.query.all()

def get_payment_by_id(payment_id: int) -> Payment:
    payment = Payment.query.get(payment_id)
    if not payment:
        raise ModelNotFoundException("Payment", payment_id)
    return payment

def add_payment(payment: Payment) -> Payment:
    db.session.add(payment)
    db.session.commit()
    return payment

def update_payment(payment: Payment) -> Payment:
    db.session.commit()
    return payment

def delete_payment(payment_id: int) -> None:
    payment = get_payment_by_id(payment_id)
    db.session.delete(payment)
    db.session.commit()