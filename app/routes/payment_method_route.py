from flask import Blueprint, jsonify, request
import controllers.payment_method_controller as controller
from utils.utils import make_error_response, need_json
from utils.exceptions import BadRequestException

payment_method = Blueprint(name="payment_method", import_name=__name__, url_prefix="/api/payment-method")

@payment_method.route("/", strict_slashes=False)
def payment_methods():
    response, status = controller.get_all_payment_methods()
    return jsonify(response), status

@payment_method.route("/<int:payment_method_id>", strict_slashes=False)
def payment_method_by_id(payment_method_id: int):
    response, status = controller.get_payment_method_by_id(payment_method_id)
    return jsonify(response), status

@payment_method.route("/", strict_slashes=False, methods=["POST"])
@need_json
def add_payment_method():
    data = request.get_json()
    response, status = controller.add_payment_method(data)
    return jsonify(response), status

@payment_method.route("/<int:payment_method_id>", strict_slashes=False, methods=["PATCH", "PUT"])
def update_payment_method(payment_method_id: int):
    if not request.is_json:
        response, status = make_error_response(BadRequestException())
        return jsonify(response), status
    
    data = request.get_json()
    response, status = controller.update_payment_method(payment_method_id, data)
    return jsonify(response), status

@payment_method.route("/<int:payment_method_id>", strict_slashes=False, methods=["DELETE"])
def delete_payment_method(payment_method_id: int):
    response, status = controller.delete_payment_method(payment_method_id)
    return jsonify(response), status