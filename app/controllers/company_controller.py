from flask import request, Response, jsonify
from utils.utils import make_error_response, is_admin_token
import services.company_service as service
from models import Company
from utils.exceptions import ModelNotFoundException, ModelAlreadyExistsException, ValidationError, InternalServerError, UnauthorizedException
import validators.company_validator as validator
import controllers.image_controller as img_controller
from werkzeug.datastructures import FileStorage
from utils.exceptions import BadRequestException

def get_all_companies():
    try:
        return [company.serialize() for company in service.get_all_companies()], 200
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def get_company_by_id(company_id: int):
    try:
        return service.get_company_by_id(company_id).serialize(), 200
    except ModelNotFoundException as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def search_company_by_name(name: str):
    try:
        companies = service.search_company_by_name(name)
        return [company.serialize() for company in companies], 200
    except ModelNotFoundException as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def delete_company(company_id: int):
    try:
        return service.delete_company(company_id), 204
    except (ModelNotFoundException, UnauthorizedException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def add_company(data):
    try:
        validated_data = validator.validate_add_company(data)
        company = service.add_company(Company(**validated_data))
        return company.serialize(), 201
    except (ValidationError, ModelAlreadyExistsException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def update_company(company_id: int, data):
    try:
        company = service.get_company_by_id(company_id)
        
        validated_data = validator.validate_update_company(data)
        
        company.name = validated_data.get("name", company.name)
        company.logo = validated_data.get("logo", company.logo)
        company.description = validated_data.get("description", company.description)
        
        company.id = company_id
        
        return service.update_company(company).serialize(), 200
    except (ValidationError, ModelNotFoundException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    

def upload_company_image(company_id: str, image: FileStorage):
    try:
        company = service.get_company_by_id(company_id)
        
        if not company:
            raise ModelNotFoundException("Company", company_id)
        
        img = img_controller.save_image(image, filename=company.name)
        
        if company.logo:
            img_controller.delete_image(company.logo.split("/")[-1])
        
        company.logo = f"{request.url_root}api/company/image/{img.id}"
        
        company = service.update_company(company)
        
        return company.serialize(), 201
    except (ModelNotFoundException, BadRequestException, UnauthorizedException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def get_company_image(image_id: int):
    try:
        image = img_controller.get_image(image_id)
        return Response(image.img, mimetype=image.mimetype), 200
    except (ModelNotFoundException, BadRequestException) as e:
        error, status = make_error_response(e)
        return jsonify(error), status
    except Exception as e:
        error, status = make_error_response(InternalServerError(str(e)))
        return jsonify(error), status