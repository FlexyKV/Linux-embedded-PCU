from flask import Blueprint
from flask_cors import CORS

from src.web.api.login_validation.login_validation import verify_token
from src.web.service.record_service import RecordService
from src.repository.record.record_repository import RecordRepository
from src.repository.database_client.database_client import DatabaseClient, database_type
from src.config.config import set_memory_type

bp = Blueprint('record', __name__, url_prefix='/record', )
CORS(bp)

db_client = DatabaseClient(database_type.record)
db_client.initialise_db()
record_repo = RecordRepository(db_client)
record_service = RecordService(record_repo)


# TODO handle errors (not date..)

@bp.route('/port/<int:port_id>/start_time/<start_time>/end_time/<end_time>/period/<int:period>', methods=['GET'])
def get_port_records(port_id, start_time, end_time, period):
    return record_service.get_port_records(port_id, start_time, end_time, period)


@bp.route('/instant', methods=['GET'])
def get_instant_record():
    return record_service.get_instant_record()


@bp.route('/memory_type/<mem_type>', methods=['PUT'])
@verify_token
def put_memory_type(mem_type):
    return set_memory_type(mem_type)


