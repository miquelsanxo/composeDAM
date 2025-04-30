from flask import request, Response, jsonify
from utils.utils import make_error_response, is_admin_token
import services.user_service as service
from models import User
from utils.exceptions import ModelNotFoundException, ModelAlreadyExistsException, ValidationError, InternalServerError, UnauthorizedException, BadRequestException
from validators import user_validator as validator
from utils.firebase_utils import verify_token_username
from werkzeug.datastructures import FileStorage
import controllers.image_controller as img_controller

def get_all_users():
    try:
        return [user.serialize() for user in service.get_all_users()], 200
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def get_user_by_username(username: str):
    try:
        user = service.get_user_by_username(username)
        if not user:
            raise ModelNotFoundException("User", username)
        return user.serialize(), 200
    except ModelNotFoundException as e:
        return make_error_response(e)
    
def search_user_by_username(username: str):
    try:
        return [user.serialize() for user in service.search_user_by_username(username)], 200
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def add_user(data: dict):
    try:
        validated_data = validator.validate_add_user(data)
        user = User(**validated_data)
        new_user = service.add_user(user)
        return new_user.serialize(), 201
    except (ModelAlreadyExistsException, ValidationError) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
    
def delete_user(username: str):
    try:
        if not is_admin_token():
            if not verify_token_username(username):
                raise UnauthorizedException()
        
        return service.delete_user_by_username(username), 204
    except (ModelNotFoundException, UnauthorizedException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def update_user(username: str, data: dict):
    try:
        if not is_admin_token():
            if not verify_token_username(username):
                raise UnauthorizedException()
        
        validated_data = validator.validate_update_user(data)
        user = service.get_user_by_username(username)
        
        user.full_name = validated_data.get("full_name", user.full_name)
        user.birth_date = validated_data.get("birth_date", user.birth_date)
        user.profile_picture = validated_data.get("profile_picture", user.profile_picture)
        user.phone = validated_data.get("phone", user.phone)
        
        new_user = service.update_user(user)
        return new_user.serialize(), 201
    except (ModelAlreadyExistsException, ModelNotFoundException, ValidationError, UnauthorizedException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def upload_user_image(username: str, image: FileStorage):
    try:
        if not is_admin_token():
            if not verify_token_username(username):
                raise UnauthorizedException()
        
        img = img_controller.save_image(image, filename=username)
        
        user = service.get_user_by_username(username)
        
        if not user:
            raise ModelNotFoundException("User", username)
        
        if user.profile_picture:
            img_controller.delete_image(user.profile_picture.split("/")[-1])
        
        user.profile_picture = f"{request.url_root}api/user/image/{img.id}"
        
        user = service.update_user(user)
        
        return user.serialize(), 201
    except (ModelNotFoundException, BadRequestException, UnauthorizedException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def get_user_image(image_id: int):
    try:
        image = img_controller.get_image(image_id)
        return Response(image.img, mimetype=image.mimetype), 200
    except (ModelNotFoundException, BadRequestException) as e:
        error, status = make_error_response(e)
        return jsonify(error), status
    except Exception as e:
        error, status = make_error_response(InternalServerError(str(e)))
        return jsonify(error), status