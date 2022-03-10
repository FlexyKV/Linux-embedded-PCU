import json
from flask import request, Blueprint
from flask_cors import CORS
from src.web.service.record_service import RecordService
from src.repository.web.record_repository import RecordRepository
from src.repository.database_client.database_client import DatabaseClient

bp = Blueprint('record', __name__, url_prefix='/record', )
CORS(bp)

db_client = DatabaseClient()
record_repo = RecordRepository(db_client)
record_service = RecordService(record_repo)


# TODO handle errors (not date..)

@bp.route('/measures', methods=['POST'])
def get_port_measures():
    payload = json.loads(request.get_data())
    return record_service.get_port_measures(payload["port_id"], payload["start_time"],
                                         payload["end_time"], payload["period"])


@bp.route('/measures', methods=['GET'])
def get_instant_measures():
    return record_service.get_instant_measures()


