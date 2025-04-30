from utils.exceptions import ValidationError
from validators.validator import Validator

def validate_add_payment_method(data: dict):
    validations = {
        "name": [Validator.is_required, Validator.is_string],
        "description": [Validator.is_required, Validator.is_string],
    }
    
    validator = Validator(data, validations)
    validated_data = validator.validate()
    
    if not validator.status:
        raise ValidationError(validator.errors)
    
    return validated_data

def validate_update_payment_method(data: dict):
    validations = {
        "name": [Validator.is_string],
        "description": [Validator.is_string],
    }
    
    validator = Validator(data, validations)
    validated_data = validator.validate()
    
    if not validator.status:
        raise ValidationError(validator.errors)
    
    return validated_data