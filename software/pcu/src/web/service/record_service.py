from src.repository.web.record_repository import RecordRepository
from src.repository.web.mapper.mapper import parse_record_to_json, MeasureMapper, str_to_datetime
import json


class RecordService:
    def __init__(self, repository: RecordRepository):
        self.repository = repository

    def get_port_measures(self, port_id: int, start_time: str, end_time: str, period: int):
        port_data = self.repository.get_port_measures(port_id, str_to_datetime(start_time), str_to_datetime(end_time))
        if port_data == -1:
            return json.dumps({"error": "no data"})

        mapper = MeasureMapper(*port_data, period, str_to_datetime(start_time), str_to_datetime(end_time))
        mapped_port_data = mapper.map_measures()
        return parse_record_to_json(mapped_port_data)

    def get_instant_measures(self):
        instant_measures = self.repository.get_instant_measures()
        # map results and handle if records is not recent
        return 1
