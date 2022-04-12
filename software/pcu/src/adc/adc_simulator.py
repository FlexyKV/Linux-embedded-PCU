import configparser
import random
from time import sleep, time

CONFIG_FILE_PATH = "/home/pi/pcu/src/config/config.ini"

#just for test
def get_reference_voltage():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    reference_voltage = config["ADC"].getfloat("reference_voltage")
    return reference_voltage


class ADCSimulator:
    def __init__(self, repo):
        self.repository = repo

    def init_repository(self):
        self.repository.create_tables()
        self.repository.create_ports()
        print("init done")

    def save_measures(self):
        current_adc = []
        voltage_adc = random.uniform(3, 5)
        power_adc = []
        for value in range(8):
            current_adc.append(random.uniform(3, 5))
            power_adc.append(random.uniform(5, 8))
        current_time = time()
        self.repository.insert_port_measures(current_time, current_adc, voltage_adc, power_adc)

    def launch_simulation(self):
        print("launch start")
        while True:
            self.save_measures()
            sleep(0.9)
