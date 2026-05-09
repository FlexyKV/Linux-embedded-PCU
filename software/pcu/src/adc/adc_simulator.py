import random
from datetime import datetime
from time import sleep, time

NUM_PORTS = 8


class ADCSimulator:
    def __init__(self, repo):
        self.repository = repo

    def init_repository(self):
        self.repository.create_tables()
        self.repository.create_ports()
        print("init done")

    def save_measures(self):
        voltage_adc = random.uniform(3, 5)
        current_adc = [random.uniform(3, 5) for _ in range(NUM_PORTS)]
        power_adc = [random.uniform(5, 8) for _ in range(NUM_PORTS)]
        self.repository.insert_port_measures(
            datetime.fromtimestamp(time()), current_adc, voltage_adc, power_adc
        )

    def launch_simulation(self):
        print("launch start")
        while True:
            self.save_measures()
            sleep(0.9)
