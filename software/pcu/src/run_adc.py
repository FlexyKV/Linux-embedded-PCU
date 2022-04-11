import configparser
from repository.adc.adc_repository import AdcRepository
from adc.mcp3008 import ADC_setup, calculate_read
from repository.database_client.database_client import DatabaseClient, CONFIG_FILE_PATH, database_type


def get_reference_voltage():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    reference_voltage = config["ADC"].getfloat("reference_voltage")
    return reference_voltage


record_db_client = DatabaseClient(database_type.record)
record_db_client.initialise_db()
port_db_client = DatabaseClient(database_type.port)
adc_repo = AdcRepository(record_db_client, port_db_client)


adc_port = ADC_setup()
while (1):
    calculate_read(adc_port, adc_repo, get_reference_voltage())
