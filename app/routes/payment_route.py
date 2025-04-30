from flask import Blueprint, jsonify, request
import controllers.payment_controller as controller
from utils.utils import make_error_response, need_json
from utils.exceptions import BadRequestException

payment = Blueprint(name="payment", import_name=__name__, url_prefix="/api/payment")

@payment.route("/", strict_slashes=False)
def payments():
    response, status = controller.get_all_payments()
    return jsonify(response), status

@payment.route("/<int:payment_id>", strict_slashes=False)
def payment_by_id(payment_id: int):
    response, status = controller.get_payment_by_id(payment_id)
    return jsonify(response), status

@payment.route("/", strict_slashes=False, methods=["POST"])
@need_json
def add_payment():
    data = request.get_json()
    response, status = controller.add_payment(data)
    return jsonify(response), status

@payment.route("/<int:payment_id>", strict_slashes=False, methods=["PATCH", "PUT"])
def update_payment(payment_id: int):
    if not request.is_json:
        response, status = make_error_response(BadRequestException())
        return jsonify(response), status
    
    data = request.get_json()
    response, status = controller.update_payment(payment_id, data)
    return jsonify(response), status

@payment.route("/<int:payment_id>", strict_slashes=False, methods=["DELETE"])
def delete_payment(payment_id: int):
    response, status = controller.delete_payment(payment_id)
    return jsonify(response), status