from flask import Blueprint, jsonify, request
import controllers.specialization_controller as controller
from utils.utils import make_error_response, need_json
from utils.exceptions import BadRequestException


specialization = Blueprint(name="specialization", import_name=__name__, url_prefix="/api/specialization")

@specialization.route("/", strict_slashes=False)
def specializations():
    response, status = controller.get_all_specializations()
    return jsonify(response), status

@specialization.route("/<int:specialization_id>", strict_slashes=False)
def specialization_by_id(specialization_id):
    response, status = controller.get_specialization_by_id(specialization_id)
    return jsonify(response), status

@specialization.route("/", strict_slashes=False, methods=["POST"])
def new_specialization():
    if not request.is_json:
        response, status = make_error_response(BadRequestException())
        return jsonify(response), status
    
    data = request.get_json()
    
    response, status = controller.create_specialization(data)
    return jsonify(response), status

@specialization.route("/search/<string:name>", strict_slashes=False)
def specialization_by_name(name):
    response, status = controller.search_specialization_by_name(name)
    return jsonify(response), status

@specialization.route("/<int:specialization_id>", strict_slashes=False, methods=["DELETE"])
def delete_specialization(specialization_id):
    response, status = controller.delete_specialization(specialization_id)
    return jsonify(response), status