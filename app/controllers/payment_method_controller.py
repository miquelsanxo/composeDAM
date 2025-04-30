from utils.utils import make_error_response
import services.payment_method_service as service
from models.payment_method import PaymentMethod
from utils.exceptions import ModelNotFoundException, ValidationError, InternalServerError
from flask import jsonify, request
from validators import payment_method_validator as validator

def get_all_payment_methods():
    try:
        return [payment_method.serialize() for payment_method in service.get_all_payment_methods()], 200
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def get_payment_method_by_id(payment_method_id: int):
    try:
        return service.get_payment_method_by_id(payment_method_id).serialize(), 200
    except ModelNotFoundException as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def add_payment_method(data: dict):
    try:
        validated_data = validator.validate_add_payment_method(data)
        payment_method = PaymentMethod(**validated_data)
        payment_method = service.add_payment_method(payment_method)
        return payment_method.serialize(), 201
    except ValidationError as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def update_payment_method(payment_method_id: int, data: dict):
    try:
        validated_data = validator.validate_update_payment_method(data)
        payment_method = service.get_payment_method_by_id(payment_method_id)
        for key, value in validated_data.items():
            setattr(payment_method, key, value)
        updated_payment_method = service.update_payment_method(payment_method)
        return updated_payment_method.serialize(), 200
    except (ValidationError, ModelNotFoundException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def delete_payment_method(payment_method_id: int):
    try:        
        service.delete_payment_method(payment_method_id)
        return '', 204
    except ModelNotFoundException as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))