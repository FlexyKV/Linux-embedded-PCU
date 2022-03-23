from flask import Blueprint
from flask_cors import CORS
from src.web.service.record_service import RecordService
from src.repository.record.record_repository import RecordRepository
from src.repository.database_client.database_client import DatabaseClient

bp = Blueprint('record', __name__, url_prefix='/record', )
CORS(bp)

db_client = DatabaseClient("record")
record_repo = RecordRepository(db_client)
record_service = RecordService(record_repo)


# TODO handle errors (not date..)

@bp.route('/port/<int:port_id>/start_time/<start_time>/end_time/<end_time>/period/<int:period>', methods=['GET'])
def get_port_records(port_id, start_time, end_time, period):
    return record_service.get_port_records(port_id, start_time, end_time, period)


@bp.route('/instant', methods=['GET'])
def get_instant_record():
    return record_service.get_instant_record()


