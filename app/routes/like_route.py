from flask import Blueprint, jsonify, request
import controllers.like_controller as controller
from utils.utils import make_error_response, need_json
from utils.exceptions import BadRequestException
from routes.post_route import post

like = Blueprint(name="like", import_name=__name__, url_prefix=f"{post.url_prefix}/like")

@like.route("/<int:post_id>", strict_slashes=False, methods=["POST"])
def toggle_like(post_id: int):
    response, status = controller.like_post(post_id)
    return jsonify(response), status

@like.route("/<int:post_id>", strict_slashes=False, methods=["GET"])
def post_likes(post_id: int):
    response, status = controller.post_likes(post_id)
    return jsonify(response), status