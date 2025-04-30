from flask import Blueprint, jsonify, request
import controllers.post_controller as controller
from utils.utils import need_json, make_error_response
from utils.exceptions import BadRequestException

post = Blueprint(name="post", import_name=__name__, url_prefix="/api/post")

@post.route("/", strict_slashes=False)
def posts():
    response, status = controller.get_all_posts()
    return jsonify(response), status

@post.route("/", strict_slashes=False, methods=["POST"])
@need_json
def add_post():
    data = request.get_json()
    
    response, status = controller.add_post(data)
    return jsonify(response), status

@post.route("/<int:post_id>", strict_slashes=False)
def post_by_id(post_id: int):
    response, status = controller.get_post_by_id(post_id)
    return jsonify(response), status

@post.route("/<int:post_id>", strict_slashes=False, methods=["DELETE"])
def delete_post(post_id: int):
    response, status = controller.delete_post(post_id)
    return jsonify(response), status

@post.route("/<int:post_id>", strict_slashes=False, methods=["PATCH", "PUT"])
def update_post(post_id: str):
    if not request.is_json:
        response, status = make_error_response(BadRequestException())
        return jsonify(response), status
    
    data = request.get_json()
    
    response, status = controller.update_post(data, post_id)
    return jsonify(response), status

@post.route("/<int:post_id>/image", strict_slashes=False, methods=["POST"])
def upload_post_image(post_id: str):
    image = request.files.get('image', None)
    
    response, status = controller.upload_post_image(post_id, image)
    return jsonify(response), status

@post.route("/image/<int:image_id>", strict_slashes=False, methods=["GET"])
def get_post_image(image_id: int):
    return controller.get_post_image(image_id)  