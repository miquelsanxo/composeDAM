from utils.db import db
from models.payment_method import PaymentMethod
from utils.exceptions import ModelNotFoundException

def get_all_payment_methods() -> list:
    return PaymentMethod.query.all()

def get_payment_method_by_id(payment_method_id: int) -> PaymentMethod:
    payment_method = PaymentMethod.query.get(payment_method_id)
    if not payment_method:
        raise ModelNotFoundException("PaymentMethod", payment_method_id)
    return payment_method

def add_payment_method(payment_method: PaymentMethod) -> PaymentMethod:
    db.session.add(payment_method)
    db.session.commit()
    return payment_method

def update_payment_method(payment_method: PaymentMethod) -> PaymentMethod:
    db.session.commit()
    return payment_method

def delete_payment_method(payment_method_id: int) -> None:
    payment_method = get_payment_method_by_id(payment_method_id)
    db.session.delete(payment_method)
    db.session.commit()