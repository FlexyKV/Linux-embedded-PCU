import json
from software.pcu.src.repository.pcu_repository import PcuRepository
import datetime

class PcuService:
    def __init__(self, repository: PcuRepository):
        self.repository = repository

    def get_pcu_port_measures(self, port_number: int, start_time: datetime, end_time: datetime):
        return 'empty.'


    def port_control(port_nb, state):
        return 'empty.'


    def get_events(port_nb, event_type, period):
        return 'empty.'


    def get_ports_states():
        return 'empty.'


    def get_ports_powers():
        return 'empty.'
