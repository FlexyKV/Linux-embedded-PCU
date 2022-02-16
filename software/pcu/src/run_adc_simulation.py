from repository.pcu_repository import PcuRepository
from adc.adc_simulator import ADCSimulator

# db_file_path = r"/home/pi/pcu/PCUDB"
db_file_path = r"C:\Users\FlexyFlex\PycharmProjects\Linux-embeded-PCU\software\pcu\PCUDB"

pcu_adc_repo = PcuRepository(db_file_path)
pcu_adc_repo.create_tables()
pcu_adc_repo.create_ports()
pcu_adc = ADCSimulator(pcu_adc_repo)
pcu_adc.launch_simulation(10)

# adc_thread = threading.Thread(target=pcu_adc.launch_simulation, args=(10,))