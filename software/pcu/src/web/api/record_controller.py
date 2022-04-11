import json
from flask import Blueprint
from flask_cors import CORS
from src.repository.record.mapper.mapper import str_to_datetime
from src.web.service.record_service import RecordService
from src.repository.record.record_repository import RecordRepository
from src.repository.database_client.database_client import DatabaseClient, database_type

bp = Blueprint('record', __name__, url_prefix='/record', )
CORS(bp)

db_client = DatabaseClient(database_type.record)
record_repo = RecordRepository(db_client)
record_service = RecordService(record_repo)


@bp.route('/port/<int:port_id>/start_time/<start_time>/end_time/<end_time>/period/<int:period>', methods=['GET'])
def get_port_records(port_id, start_time, end_time, period):
    try:
        str_to_datetime(start_time)
        str_to_datetime(end_time)
    except:
        return json.dumps({"error": "invalid date ('%Y-%m-%dT%H:%M:%S.%fZ')"})
    return record_service.get_port_records(port_id, start_time, end_time, period)


@bp.route('/instant', methods=['GET'])
def get_instant_record():
    return record_service.get_instant_record()

