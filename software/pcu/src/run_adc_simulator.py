from repository.adc.adc_repository import AdcRepository
from adc.adc_simulator import ADCSimulator
from repository.database_client.database_client import DatabaseClient, database_type


record_db_client = DatabaseClient(database_type.record)
record_db_client.initialise_db()
port_db_client = DatabaseClient(database_type.port)


adc_repo = AdcRepository(record_db_client, port_db_client)
adc = ADCSimulator(adc_repo)
adc.launch_simulation()