from repository.database_client.database_client import DatabaseClient, database_type
from repository.ports.ports_repository import PortsRepository
from web.ports.pcu_ports import gpio_setup, gpio_toggle_off, gpio_toggle_on

port_db_client = DatabaseClient(database_type.port)
port_db_client.initialise_db()
port_repo = PortsRepository(port_db_client)
gpio_setup()

for port_id in range(8):
    state = port_repo.get_port_state(port_id)
    if state == 1:
        gpio_toggle_on(port_id)
    elif state == 0:
        gpio_toggle_off(port_id)
