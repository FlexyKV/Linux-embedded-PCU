import json
from flask import request, Blueprint
from flask_cors import CORS
from src.web.service.ports_service import PortsService
from src.repository.web.ports_repository import PortsRepository
from src.repository.database_client.database_client import DatabaseClient

bp = Blueprint('ports', __name__, url_prefix='/ports', )
CORS(bp)

db_client = DatabaseClient()
ports_repo = PortsRepository(db_client)
ports_service = PortsService(ports_repo)

# TODO handle errors


@bp.route('/state', methods=['POST'])
def get_port_state():
    payload = json.loads(request.get_data())
    return ports_service.get_port_state(payload["port_id"])


@bp.route('/state', methods=['PUT'])
def put_port_state():
    payload = json.loads(request.get_data())
    return ports_service.update_port_state(payload["port_id"], payload["port_state"])
