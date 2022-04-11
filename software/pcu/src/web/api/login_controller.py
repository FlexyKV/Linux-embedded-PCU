import json
from flask import Blueprint, make_response
from flask_cors import CORS
from src.config.config import get_login_password
from src.web.api.login_validation.login_validation import validate_access, algo_encryption
import jwt
import datetime

bp = Blueprint('login', __name__, url_prefix='/login', )
CORS(bp)


@bp.route('/<password>', methods=['GET'])
def login(password):
    if validate_access(password):
        token = jwt.encode(
            {'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10)}, get_login_password(),
            algorithm=algo_encryption)
        response = {
            "status": 200,
            "token": token
        }
        return json.dumps(response)

    return make_response('Wrong password', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
