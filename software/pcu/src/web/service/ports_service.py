from src.repository.ports.ports_repository import PortsRepository
from src.repository.record.mapper.mapper import parse_port_state_to_json
from src.web.ports.pcu_ports import gpio_setup, gpio_toggle_off, gpio_toggle_on


class PortsService:
    def __init__(self, repository: PortsRepository):
        self.repository = repository
        gpio_setup()

    def get_port_state(self, port_id: int):
        """Get the state of port_id."""
        port_state = self.repository.get_port_state(port_id)
        return parse_port_state_to_json(port_id, port_state)

    def update_port_state(self, port_id: int, state: int):
        """Apply the state on the GPIO, then persist it."""
        if state:
            gpio_toggle_on(port_id)
        else:
            gpio_toggle_off(port_id)

        new_state = self.repository.update_port_state(port_id, state)
        return parse_port_state_to_json(port_id, new_state)
