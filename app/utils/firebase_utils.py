import pyrebase
from config import FIREBASECONFIG, ADMIN_TOKEN
from requests.exceptions import HTTPError
from utils.exceptions import FirebaseException, UnauthorizedException, BadRequestException
from flask import request
from models import User
from utils.constants import TOKEN_REQUIRED
from services.user_service import get_user_by_uid

firebase = pyrebase.initialize_app(FIREBASECONFIG)
auth = firebase.auth()

def get_uid_by_token(token: str) -> str:
    try:
        user = auth.get_account_info(token)
        return user['users'][0]['localId']
    except HTTPError as e:
        raise FirebaseException(e)
    
def verify_token_username(username: str) -> bool:
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        raise BadRequestException(TOKEN_REQUIRED)
    
    uid = get_uid_by_token(auth_header)
    user = get_user_by_uid(uid)
    
    return user.username == username

def verify_token_uid(uid: str) -> bool:
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        raise BadRequestException(TOKEN_REQUIRED)
    
    if auth_header == ADMIN_TOKEN:
        return True
    
    return get_uid_by_token(auth_header) == uid

def get_user_by_token() -> User:
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        raise BadRequestException(TOKEN_REQUIRED)
    
    uid_user = get_uid_by_token(auth_header)
    return get_user_by_uid(uid_user)