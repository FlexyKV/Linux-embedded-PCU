from src.repository.pcu_repository import PcuRepository
from src.service.mapper.mapper import parse_record_to_json, MeasureMapper, str_to_datetime, \
    parse_port_state_to_json
import json


class PcuService:
    def __init__(self, repository: PcuRepository):
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

    def get_port_state(self, port_id: int):
        port_state = self.repository.get_port_state(port_id)
        return parse_port_state_to_json(port_id, port_state)

    def update_port_state(self, port_id: int, state: int):
        # first launch GPIO state change

        # if ok change state in repo
        state = self.repository.update_port_state(port_id, state)
        return parse_port_state_to_json(port_id, state)
