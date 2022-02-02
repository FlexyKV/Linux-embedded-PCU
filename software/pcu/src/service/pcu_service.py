from software.pcu.src.repository.pcu_repository import PcuRepository
from software.pcu.src.service.mapper import port_measure_mapper, port_state_mapper, str_to_datetime
import json


class PcuService:
    def __init__(self, repository: PcuRepository):
        self.repository = repository

    def get_port_measures(self, port_id: int, start_time: str, end_time: str, period: int):
        measures = self.repository.get_port_measures(port_id, str_to_datetime(start_time), str_to_datetime(end_time), period)
        if measures == -1:
            return json.dumps({"error": "no data"})
        return port_measure_mapper(measures)

    def get_port_state(self, port_id: int):
        port_state = self.repository.get_port_state(port_id)
        return port_state_mapper(port_id, port_state)

    def update_port_state(self, port_id: int, state: int):
        # first launch GPIO state change

        # if ok change state in repo
        state = self.repository.update_port_state(port_id, state)
        return port_state_mapper(port_id, state)
