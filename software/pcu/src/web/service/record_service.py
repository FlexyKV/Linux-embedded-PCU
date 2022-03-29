from src.repository.record.record_repository import RecordRepository
from src.repository.record.mapper.mapper import parse_record_to_json, MeasureMapper, str_to_datetime, parse_instant_record_to_json
import json


class RecordService:
    def __init__(self, repository: RecordRepository):
        self.repository = repository

    def get_port_records(self, port_id: int, start_time: str, end_time: str, period: int):
        port_data = self.repository.get_port_records(port_id, str_to_datetime(start_time), str_to_datetime(end_time))
        if port_data == -1:
            return json.dumps({"error": "no data"})

        mapper = MeasureMapper(*port_data, period, str_to_datetime(start_time), str_to_datetime(end_time))
        mapped_port_data = mapper.map_measures()
        return parse_record_to_json(mapped_port_data)

    def get_instant_record(self):
        instant_measures = self.repository.get_instant_record()
        if instant_measures == -1:
            return json.dumps({"error": "no data"})

        return parse_instant_record_to_json(*instant_measures)
