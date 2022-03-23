from repository.adc.adc_repository import AdcRepository
from adc.adc_simulator import ADCSimulator
from repository.database_client.database_client import DatabaseClient

db_client = DatabaseClient()
adc_repo = AdcRepository(db_client)
adc = ADCSimulator(adc_repo)
adc.launch_simulation(10)

# adc_thread = threading.Thread(target=pcu_adc.launch_simulation, args=(10,))