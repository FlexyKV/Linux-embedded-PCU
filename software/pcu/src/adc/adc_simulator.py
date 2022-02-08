import random
import datetime
from time import sleep


class ADCSimulator:
    def __init__(self, repo):
        self.repository = repo

    def init_repository(self):
        self.repository.create_tables()
        self.repository.create_ports()
        print("init done")

    def save_measures(self):
        current_adc = []
        voltage_adc = []
        for value in range(8):
            current_adc.append(random.uniform(3, 5))
            voltage_adc.append(random.uniform(3, 5))
        current_time = datetime.datetime.now()
        self.repository.insert_port_measures(current_time, 1, current_adc, voltage_adc)

    def launch_simulation(self, simulation_time):
        print("launch start")
        elapsed_time = 0
        while True: #simulation_time - elapsed_time > 0:
            self.save_measures()
            elapsed_time += 1
            print(f"measure save {elapsed_time}")
            sleep(1)
        # print("launch end")
