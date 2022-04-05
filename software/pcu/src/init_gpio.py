from repository.ports.ports_repository import PortsRepository
from repository.database_client.database_client import DatabaseClient, database_type
from web.ports.pcu_ports import gpio_toggle_ON, gpio_toggle_OFF, gpio_setup


port_db_client = DatabaseClient(database_type.port)
port_repo = PortsRepository(port_db_client)
gpio_setup()

for i in range(8):
    port_state = port_repo.get_port_state(i)
    if port_state == 1:
        gpio_toggle_ON(i)
    elif port_state == 0:
        gpio_toggle_OFF(i)
