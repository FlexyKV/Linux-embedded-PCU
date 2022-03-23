from repository.adc.adc_repository import AdcRepository
from adc.mcp3008 import ADC_setup, calculate_read
from repository.database_client.database_client import DatabaseClient


adc_port = ADC_setup()

record_db_client = DatabaseClient("record")
try:
    record_db_client.initialise_db()
except:
    pass
port_db_client = DatabaseClient("port")
try:
    port_db_client.initialise_db()
except:
    pass

adc_repo = AdcRepository(record_db_client, port_db_client)

while (1):
    calculate_read(adc_port, adc_repo)
