import json
from flask import request, Blueprint
from flask_cors import CORS
from src.web.service.ports_service import PortsService
from src.repository.ports.ports_repository import PortsRepository
from src.repository.database_client.database_client import DatabaseClient, database_type
from src.web.api.login_validation.login_validation import verify_token

bp = Blueprint('ports', __name__, url_prefix='/port', )
CORS(bp)

db_client = DatabaseClient(database_type.port)
ports_repo = PortsRepository(db_client)
ports_service = PortsService(ports_repo)

# TODO handle errors


@bp.route('/<int:port_id>/state', methods=['GET'])
def get_port_state(port_id):
    return ports_service.get_port_state(port_id)


@bp.route('/state', methods=['PUT'])
@verify_token
def put_port_state():
    payload = json.loads(request.get_data())
    return ports_service.update_port_state(payload["port_id"], payload["port_state"])
