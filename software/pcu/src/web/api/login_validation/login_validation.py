from flask import request, make_response
from functools import wraps
import jwt
from src.config.config import get_login_password


algo_encryption = "HS256"


def validate_access(passwd):
    if passwd == get_login_password():
        return True
    return False


def verify_authorization():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        try:
            jwt.decode(token, get_login_password(), algorithms=algo_encryption)
        except:
            return False
    if not token:
        return False
    return True


def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        has_permission = verify_authorization()
        if has_permission:
            return f(*args, **kwargs)
        return make_response('Permission required', 401)
    return decorated
