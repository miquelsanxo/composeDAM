from utils.utils import make_error_response
import services.payment_service as service
from models.payment import Payment
from utils.exceptions import ModelNotFoundException, ValidationError, InternalServerError
from flask import jsonify, request
from validators import payment_validator as validator
from utils.firebase_utils import get_user_by_token

def get_all_payments():
    try:
        return [payment.serialize() for payment in service.get_all_payments()], 200
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def get_payment_by_id(payment_id: int):
    try:
        return service.get_payment_by_id(payment_id).serialize(), 200
    except ModelNotFoundException as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def add_payment(data: dict):
    try:
        validated_data = validator.validate_add_payment(data)
        
        user = get_user_by_token()
        
        if not user:
            raise ModelNotFoundException("User", "user")
        
        if user.id == validated_data.get("user2_id", None):
            raise ValidationError({"user2_id": "User cannot be the same as user2_id"})
        
        payment = Payment(**validated_data)
        payment.user1_id = user.id
        
        payment = service.add_payment(payment)
        return payment.serialize(), 201
    except (ValidationError, ModelNotFoundException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def update_payment(payment_id: int, data: dict):
    try:
        validated_data = validator.validate_update_payment(data)
        payment = service.get_payment_by_id(payment_id)
        for key, value in validated_data.items():
            setattr(payment, key, value)
        updated_payment = service.update_payment(payment)
        return updated_payment.serialize(), 200
    except (ValidationError, ModelNotFoundException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def delete_payment(payment_id: int):
    try:        
        service.delete_payment(payment_id)
        return '', 204
    except ModelNotFoundException as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))