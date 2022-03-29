from flask import Blueprint
from flask_cors import CORS
from src.web.api.login_validation.login_validation import verify_token
from src.config.config import set_reference_voltage

bp = Blueprint('adc', __name__, url_prefix='/adc', )
CORS(bp)


@bp.route('/reference_voltage/<reference_voltage>', methods=['PUT'])
@verify_token
def put_reference_voltage(reference_voltage):
    return set_reference_voltage(reference_voltage)
