from utils.exceptions import ValidationError
from validators.validator import Validator

def validate_add_user(data: dict):
    validations = {
        "uid": [Validator.is_required, Validator.is_string],
        "full_name": [Validator.is_required, Validator.is_string],
        "username": [Validator.is_required, Validator.is_string],
        "birth_date": [Validator.is_required, Validator.is_date],
        "email": [Validator.is_required, Validator.is_email],
        "phone": [Validator.is_required, Validator.is_string],
        "profile_picture": [Validator.is_string],
    }
    
    validator = Validator(data, validations)
    validated_data = validator.validate()
    
    if not validator.status:
        raise ValidationError(validator.errors)
    
    return validated_data
    
def validate_update_user(data: dict):
    validations = {
        "full_name": [Validator.is_string],
        "birth_date": [Validator.is_date],
        "phone": [Validator.is_string],
        "profile_picture": [Validator.is_string],
    }
    
    validator = Validator(data, validations)
    validated_data = validator.validate()
    
    if not validator.status:
        raise ValidationError(validator.errors)
    
    return validated_data