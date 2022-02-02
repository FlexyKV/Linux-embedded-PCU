from datetime import datetime
from repository.pcu_repository import PcuRepository
from adc.adc_simulator import ADCSimulator


""" file to manually test database interactions """

db_file_path = r"C:\Users\FlexyFlex\PycharmProjects\Linux-embeded-PCU\software\pcu\PCUDB"

repo = PcuRepository(db_file_path)
simulator = ADCSimulator(repo)

simulator.init_repository()
old_time = datetime.now()
simulator.launch_simulation(5)


# repo.open_connection()
# measures = repo.get_port_measures(1, old_time, datetime.now(), 1)
# measures2 = repo.get_port_measures(2, old_time, datetime.now(), 1)
# repo.close_connexion()
# print(measures)
# print(measures2)
