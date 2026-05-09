import configparser

from adc.mcp3008 import adc_setup, calculate_read
from repository.adc.adc_repository import AdcRepository
from repository.database_client.database_client import (
    CONFIG_FILE_PATH,
    DatabaseClient,
    database_type,
)


def get_reference_voltage():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    return config["ADC"].getfloat("reference_voltage")


record_db_client = DatabaseClient(database_type.record)
record_db_client.initialise_db()
port_db_client = DatabaseClient(database_type.port)
adc_repo = AdcRepository(record_db_client, port_db_client)

adc_port = adc_setup()

# Re-read the reference voltage every cycle so /config/reference_voltage edits
# take effect without a restart.
while True:
    calculate_read(adc_port, adc_repo, get_reference_voltage())
