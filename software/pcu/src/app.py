from datetime import datetime
from repository.pcu_repository import PcuRepository
from adc.adc_simulator import ADCSimulator

db_file_path = r"C:\Users\FlexyFlex\PycharmProjects\Linux-embeded-PCU\software\pcu\PCUDB"

repo = PcuRepository(db_file_path)
simulator = ADCSimulator(repo)

repo.open_connection()
simulator.init_repository()
old_time = datetime.now()
simulator.launch_simulation(4)
repo.close_connexion()

repo.open_connection()
measures = repo.get_port_measures(1, old_time, datetime.now(), 1)
repo.close_connexion()
print(measures)