import json
from flask import Blueprint, request


bp = Blueprint('pcu', __name__, url_prefix='/')


@bp.route('', methods=['GET'])
def test():
    return 'empty.'


@bp.route('/ports', methods=['PUT'])
def put_port_control():
    payload = json.loads(request.get_data())
    return 'empty.'


@bp.route('/events', methods=['GET'])
def get_events():
    payload = json.loads(request.get_data())
    return 'empty.'


@bp.route('/ports', methods=['GET'])
def get_ports_states():
    return 'empty.'


@bp.route('/ports/power', methods=['GET'])
def get_ports_powers():
    return 'empty.'
