from datetime import datetime
from utils.constants import *
from services import *
from utils.exceptions import ModelNotFoundException

class Validator:
    def __init__(self, data: dict, validations: dict):
        self.status = True
        self.errors = []
        self.data = data
        self.validations = validations
        
    def validate(self) -> dict:
        data = {}
        for key, value in self.validations.items():
            if not value[0] is Validator.is_required and self.data.get(key, None) is None:
                continue
            
            for validation in value:
                field = self.data.get(key, None)
                if isinstance(validation, list):
                    status, message = validation[0](self, field, validation[1])
                else:
                    status, message = validation(self, field)
                if not status:
                    self.add_error(key, message)
                    break
                
                data[key] = field
        return data
    
    def is_required(self, value):
        if value is None or value == "":
            return False, IS_REQUIRED
        return True, ''
    
    def is_number(self, value):
        try:
            float(str(value).replace(',', '.'))
            return True, ''
        except ValueError:
            return False, IS_NUMBER
    
    def positive_number(self, value):
        if float(value) < 0:
            return False, POSITIVE_NUMBER
        return True, ''
    
    def is_string(self, value):
        if not isinstance(value, str):
            return False, IS_STRING
        return True, ''
    
    def is_date(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return False, IS_DATE
        return True, ''
    
    def is_email(self, value):
        if not '@' in value or not '.' in value:
            return False, IS_EMAIL
        return True, ''
    
    def is_boolean(self, value):
        if not isinstance(value, bool) and not value in ["True", "False"] and not value in [1, 0]:
            return False, IS_BOOLEAN
        value = value == "True" or value == 1
        return True, ''
    
    def equals(self, value, values):
        if value not in values:
            return False, f'The field must be one of the following values: {values}'
        return True, ''
    
    def exist_company(self, value):
        try:
            company_service.get_company_by_id(value)
            return True, ''
        except ModelNotFoundException:
            return False, f'The company with id {value} does not exist'
        except Exception as e:
            return False, str(e)
    
    def exist_specialization(self, value):
        try:
            specialization_service.get_specialization_by_id(value)
            return True, ''
        except ModelNotFoundException:
            return False, f'The specialization with id {value} does not exist'
        except Exception as e:
            return False, str(e)
    
    def exist_user(self, value):
        try:
            user_service.get_user_by_id(value)
            return True, ''
        except ModelNotFoundException:
            return False, f'The user with id {value} does not exist'
        except Exception as e:
            return False, str(e)
        
    def exist_post(self, value):
        try:
            post_service.get_post_by_id(value)
            return True, ''
        except ModelNotFoundException:
            return False, f'The post with id {value} does not exist'
        except Exception as e:
            return False, str(e)
        
    def exist_payment_method(self, value):
        try:
            payment_method_service.get_payment_method_by_id(value)
            return True, ''
        except ModelNotFoundException:
            return False, f'The payment method with id {value} does not exist'
        except Exception as e:
            return False, str(e)
    
    def add_error(self, key: str, message: str):
        self.errors.append({key: message})
        self.status = False