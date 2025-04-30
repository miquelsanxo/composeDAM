from utils.constants import BODY_REQUIRED, INTERNAL_SERVER_ERROR, METHOD_NOT_ALLOWED, UNAUTHORIZED_ERROR, VALIDATION_ERROR
from requests.exceptions import HTTPError
import json

class ModelNotFoundException(Exception):
    def __init__(self, model_name, field):
        self.model_name = model_name
        self.field = field
        self.details = f"{model_name} '{field}' not found."
        self.status_code = 404
        super().__init__(self.details)
        
class ModelAlreadyExistsException(Exception):
    def __init__(self, model_name, field):
        self.model_name = model_name
        self.field = field
        self.details = f"{model_name} '{field}' already exists."
        self.status_code = 409
        super().__init__(self.details)
        
class ValidationError(Exception):
    def __init__(self, errors: dict = {}):
        self.details = errors
        self.status_code = 400
        super().__init__(VALIDATION_ERROR)
        
class UnauthorizedException(Exception):
    def __init__(self):
        self.details = UNAUTHORIZED_ERROR
        self.status_code = 401
        super().__init__(self.details)
        
class InternalServerError(Exception):
    def __init__(self, details: str = INTERNAL_SERVER_ERROR):
        self.details = details
        self.status_code = 500
        super().__init__(details)
        
class BadRequestException(Exception):
    def __init__(self, details: str = BODY_REQUIRED):
        self.details = details
        self.status_code = 400
        super().__init__(self.details)
        
class PageNotFound(Exception):
    def __init__(self, path: str = ""):
        self.details = f"Page '{path}' not found"
        self.status_code = 404
        super().__init__(self.details)
        
class MethodNotAllowed(Exception):
    def __init__(self):
        self.details = METHOD_NOT_ALLOWED
        self.status_code = 405
        super().__init__(self.details)
        
class FirebaseException(HTTPError):
    def __init__(self, exception: HTTPError):
        error_json = exception.args[1]
        error_dict = json.loads(error_json).get('error')
        self.details = error_dict.get('message', INTERNAL_SERVER_ERROR)
        self.status_code = error_dict.get('code', 500)
        super().__init__(f"{self.status_code}: {self.details}")