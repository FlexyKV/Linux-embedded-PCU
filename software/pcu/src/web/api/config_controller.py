import json

from flask import Blueprint
from flask_cors import CORS

from src.repository.database_client.database_client import get_record_memory_type
from src.web.api.login_validation.login_validation import verify_token
from src.config.config import set_reference_voltage, set_memory_type, set_log_ip, set_log_port, set_login_password, \
    reboot_pcu, get_ip

bp = Blueprint('config', __name__, url_prefix='/config', )
CORS(bp)


@bp.route('/memory_type/<mem_type>', methods=['PUT'])
@verify_token
def put_memory_type(mem_type):
    """modify the memory type in the config file"""
    return set_memory_type(mem_type)


@bp.route('/memory_type', methods=['GET'])
def get_memory_type():
    """get the memory type from the config file"""
    mem_type = get_record_memory_type()
    return json.dumps({"status": 200, "mem_type": str(mem_type)})


@bp.route('/log_ip/<log_ip>', methods=['PUT'])
@verify_token
def put_log_ip(log_ip):
    """modify the log ip address in the config file"""
    return set_log_ip(log_ip)


@bp.route('/log_port/<log_port>', methods=['PUT'])
@verify_token
def put_log_port(log_port):
    """modify the log port in the config file"""
    return set_log_port(log_port)


@bp.route('/password/<password>', methods=['PUT'])
@verify_token
def put_password(password):
    """modify the password in the config file"""
    return set_login_password(password)


@bp.route('/reference_voltage/<reference_voltage>', methods=['PUT'])
@verify_token
def put_reference_voltage(reference_voltage):
    """modify the reference voltage in the config file"""
    return set_reference_voltage(reference_voltage)


@bp.route('/reboot', methods=['PUT'])
@verify_token
def reboot_pi():
    """reboot the Raspberry Pi"""
    return reboot_pcu()


@bp.route('/ip', methods=['GET'])
@verify_token
def get_pcu_ip():
    """get the Raspberry Pi ip address"""
    return get_ip()
