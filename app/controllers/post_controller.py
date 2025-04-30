from utils.utils import make_error_response, is_admin_token
import services.post_service as service
from utils.exceptions import InternalServerError, ValidationError, ModelNotFoundException, UnauthorizedException, FirebaseException
import validators.post_validator as validator
from utils.firebase_utils import get_user_by_token
from models.post import Post
from utils.firebase_utils import verify_token_username
from werkzeug.datastructures import FileStorage
from flask import request, Response, jsonify
from utils.exceptions import BadRequestException
import controllers.image_controller as img_controller

def get_all_posts():
    try:
        return [post.serialize() for post in service.get_all_posts()], 200
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))

def add_post(data: dict):
    try:
        user = get_user_by_token()
        
        data['user_id'] = user.id
        
        validated_data = validator.validate_add_post(data)
        
        post = service.add_post(Post(**validated_data))
        
        return post.serialize(), 201
    except (ValidationError, FirebaseException, ModelNotFoundException, UnauthorizedException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def get_post_by_id(post_id: int):
    try:
        return service.get_post_by_id(post_id).serialize(), 200
    except ModelNotFoundException as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def delete_post(post_id: int):
    try:
        if is_admin_token():
            return service.delete_post(post_id), 204
        
        user = get_user_by_token()
        
        post = service.get_post_by_id(post_id)
        
        if post.user_id != user.id:
            raise UnauthorizedException("You are not authorized to delete this post")
        
        return service.delete_post(post_id), 204
    except (ModelNotFoundException, UnauthorizedException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def update_post(data: dict, post_id: int):
    try:
        if not is_admin_token():
            user = get_user_by_token()
        
        post = service.get_post_by_id(post_id)
        
        if not is_admin_token():
            if post.user_id != user.id:
                raise UnauthorizedException("You are not authorized to update this post")
        
        validated_data = validator.validate_update_post(data)
        
        post.title = validated_data.get("title", post.title)
        post.description = validated_data.get("description", post.description)
        post.photo = validated_data.get("photo", post.photo)
        post.specialization_id = validated_data.get("specialization_id", post.specialization_id)
        post.price = validated_data.get("price", post.price)
        post.company_id = validated_data.get("company_id", post.company_id)
        
        post.id = post_id
        
        return service.update_post(post).serialize(), 200
    except (ValidationError, ModelNotFoundException, UnauthorizedException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    

def upload_post_image(post_id: int, image: FileStorage):
    try:
        post = service.get_post_by_id(post_id)
        
        if not post:
            raise ModelNotFoundException("Post", post_id)
        
        user = get_user_by_token()
        
        if not user:
            raise ModelNotFoundException("User", "user")
        
        if not is_admin_token():
            user = get_user_by_token()
            
            post = service.get_post_by_id(post_id)
            
            if post.user_id != user.id:
                raise UnauthorizedException("You are not authorized to delete this post")
            
        img = img_controller.save_image(image, filename=post.title)
        
        if post.photo:
            img_controller.delete_image(post.photo.split("/")[-1])
        
        post.photo = f"{request.url_root}api/post/image/{img.id}"
        
        post = service.update_post(post)
        
        return post.serialize(), 201
    except (ModelNotFoundException, BadRequestException, UnauthorizedException) as e:
        return make_error_response(e)
    except Exception as e:
        return make_error_response(InternalServerError(str(e)))
    
def get_post_image(image_id: int):
    try:
        image = img_controller.get_image(image_id)
        return Response(image.img, mimetype=image.mimetype), 200
    except (ModelNotFoundException, BadRequestException) as e:
        error, status = make_error_response(e)
        return jsonify(error), status
    except Exception as e:
        error, status = make_error_response(InternalServerError(str(e)))
        return jsonify(error), status