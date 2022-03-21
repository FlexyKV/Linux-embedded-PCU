from flask import request, make_response
from functools import wraps
import jwt

key = "admin"
algo_encryption = "HS256"


def validate_access(passwd):
    if passwd == key:
        return True
    return False


def verify_authorization():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        try:
            jwt.decode(token, key, algorithms=algo_encryption)
        except jwt.exceptions.DecodeError:
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
