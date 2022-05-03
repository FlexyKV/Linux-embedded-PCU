from src.repository.ports.ports_repository import PortsRepository
from src.repository.record.mapper.mapper import parse_port_state_to_json
from src.web.ports.pcu_ports import gpio_toggle_ON, gpio_toggle_OFF, gpio_setup


class PortsService:
    def __init__(self, repository: PortsRepository):
        self.repository = repository
        gpio_setup()

    def get_port_state(self, port_id: int):
        """get the port_id state"""
        port_state = self.repository.get_port_state(port_id)
        return parse_port_state_to_json(port_id, port_state)

    def update_port_state(self, port_id: int, state: int):
        """update the port_id state on Raspberry Pi then in the database"""
        # first launch GPIO state change
        if state:
            gpio_toggle_ON(port_id)
        else:
            gpio_toggle_OFF(port_id)

        # if ok change state in repo
        state = self.repository.update_port_state(port_id, state)
        return parse_port_state_to_json(port_id, state)
