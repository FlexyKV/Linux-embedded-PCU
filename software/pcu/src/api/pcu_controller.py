import json
from flask import request, Blueprint
from flask_cors import CORS
from src.service.pcu_service import PcuService
from src.repository.pcu_repository import PcuRepository
from src.domain.ports.pcu_ports import gpio_setup

bp = Blueprint('pcu', __name__, url_prefix='/',)
CORS(bp)

db_file_path = r"/home/pi/pcu/PCUDB"
# db_file_path = r"C:\Users\FlexyFlex\PycharmProjects\Linux-embeded-PCU\software\pcu\PCUDB"
pcu_service_repo = PcuRepository(db_file_path)
pcu_service_repo.create_tables()
pcu_service_repo.create_ports()
pcu_service_repo.create_triggers()
pcu_service = PcuService(pcu_service_repo)
gpio_setup()

#pcu_logging_repo = PcuRepository(db_file_path)
#pcu_logging = loggingSyslog("192.168.1.80", 514, pcu_logging_repo)
#logging_thread = threading.Thread(target=pcu_logging.logging_valeurs())
#logging_thread.start()


@bp.route('/port_measures', methods=['POST'])
def get_port_measures():
    payload = json.loads(request.get_data())
    return pcu_service.get_port_measures(payload["port_id"], payload["start_time"],
                                         payload["end_time"], payload["period"])


@bp.route('/instant_measures', methods=['GET'])
def get_instant_measures():
    return pcu_service.get_instant_measures()


@bp.route('/port_state', methods=['POST'])
def get_port_state():
    payload = json.loads(request.get_data())
    return pcu_service.get_port_state(payload["port_id"])


@bp.route('/port_state', methods=['PUT'])
def put_port_state():
    payload = json.loads(request.get_data())
    return pcu_service.update_port_state(payload["port_id"], payload["port_state"])



