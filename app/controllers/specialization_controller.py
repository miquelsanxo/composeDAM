from flask import request
from utils.utils import make_error_response, is_admin_token
import services.specialization_service as service
from models import Specialization
import validators.specialization_validator as validator
from utils.exceptions import ModelNotFoundException, ModelAlreadyExistsException, ValidationError, InternalServerError, UnauthorizedException

def get_all_specializations():
    try:
        return [specialization.serialize() for specialization in service.get_all_specializations()], 200
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def get_specialization_by_id(specialization_id):
    try:
        specialization = service.get_specialization_by_id(specialization_id)
        return specialization.serialize(), 200
    except ModelNotFoundException as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def search_specialization_by_name(name):
    try:
        specializations = service.search_specialization_by_name(name)
        return [specialization.serialize() for specialization in specializations], 200
    except ModelNotFoundException as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def create_specialization(data):
    try:
        validated_data = validator.validate_add_specialization(data)
        specialization = service.add_specialization(Specialization(**validated_data))
        return specialization.serialize(), 201
    except (ModelAlreadyExistsException, ValidationError) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def delete_specialization(specialization_id):
    try:
        return service.delete_specialization(specialization_id), 204
    except ModelNotFoundException as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))