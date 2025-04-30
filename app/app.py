from flask import Flask, jsonify, request
from flask_cors import CORS
from config import DATABASE_CONNECTION_URI, DEBUG
from routes import *
from utils.db import db
from utils.exceptions import InternalServerError, PageNotFound, MethodNotAllowed
from utils.utils import make_error_response

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

CORS(app)

app.register_blueprint(user)
app.register_blueprint(post)
app.register_blueprint(company)
app.register_blueprint(like)
app.register_blueprint(specialization)
app.register_blueprint(payment)
app.register_blueprint(payment_method)

@app.before_request
def create_tables():
    with app.app_context():
        import models
        db.create_all()

@app.errorhandler(404)
def page_not_found(error: Exception):
    response, status = make_error_response(PageNotFound(request.path))
    return jsonify(response), status


@app.errorhandler(405)
def method_not_allowed(error: Exception):
    response, status = make_error_response(MethodNotAllowed())
    return jsonify(response), status


@app.errorhandler(Exception)
def handle_exception(error: Exception):
    response, status = make_error_response(InternalServerError(str(error)))
    return jsonify(response), status