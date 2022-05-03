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
    """get record data for port_id from start_time to end_time for every period
    return:
    { "measures": { <timestamp>: {"current": <int>, "voltage": <int>, "power": <float>}, ...},
    "avg_measure": {"current": <float>, "voltage": <float>, "power": <float>},
    "max_measure": {"current": <float>, "voltage": <float>, "power": <float>},
    "min_measure": {"current": <float>, "voltage": <float>, "power": <float>},
    "port_states": [[<timestamp>,<int>], ... ] } """

    try:
        str_to_datetime(start_time)
        str_to_datetime(end_time)
    except:
        return json.dumps({"error": "invalid date ('%Y-%m-%dT%H:%M:%S.%fZ')"})
    return record_service.get_port_records(port_id, start_time, end_time, period)


@bp.route('/instant', methods=['GET'])
def get_instant_record():
    """get last record data and port state for all ports
        return:
        { "datetime": <timestamp>,
        "port_0": {"port_state": <int>, "port_current": <float>, "port_voltage": <float>, "port_power": <float>},
        ...} """
    return record_service.get_instant_record()
