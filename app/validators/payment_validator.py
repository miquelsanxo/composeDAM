from utils.exceptions import ValidationError
from validators.validator import Validator

def validate_add_payment(data: dict):
    validations = {
        "user2_id": [Validator.is_required, Validator.is_number, Validator.exist_user],
        "post_id": [Validator.is_required, Validator.is_number, Validator.exist_post],
        "amount": [Validator.is_required, Validator.is_number, Validator.positive_number],
        "payment_date": [Validator.is_date],
        "payment_method_id": [Validator.is_required, Validator.is_number, Validator.exist_payment_method]
    }

    validator = Validator(data, validations)
    validated_data = validator.validate()

    if not validator.status:
        raise ValidationError(validator.errors)

    return validated_data

def validate_update_payment(data: dict):
    validations = {
        "amount": [Validator.is_number, Validator.positive_number],
        "payment_method_id": [Validator.is_number, Validator.exist_payment_method]
    }

    validator = Validator(data, validations)
    validated_data = validator.validate()

    if not validator.status:
        raise ValidationError(validator.errors)

    return validated_data