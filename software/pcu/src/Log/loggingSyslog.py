# myapp.py
import logging
import logging.handlers
import random
from datetime import datetime, timedelta
import sys
import threading

from software.pcu.src.service.mapper import MeasureMapper

#À mettre dans pcu_controller
#pcu_logging_repo = PcuRepository(db_file_path)
#pcu_logging = loggingSyslog("192.168.1.80", 514,pcu_logging_repo)
#logging_thread = threading.Thread(target=pcu_logging.logging_valeurs())
#logging_thread.start()


class loggingSyslog(object):

    def __init__(self, address, port,repo):
        self.address = address
        self.port = port
        self.repository = repo

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        syslog = logging.handlers.SysLogHandler(address=(self.address, self.port))
        logger.addHandler(syslog)

    def logging_valeurs(self):
        all_avg_mesures = self.get_avg_mesure()
        print("Port:" , all_avg_mesures[0][0], "Currents:", all_avg_mesures[0][1], "Power:", all_avg_mesures[0][2])
        print("Port:", all_avg_mesures[1][0], "Currents:", all_avg_mesures[1][1], "Power:", all_avg_mesures[1][2])
        print("Port:", all_avg_mesures[2][0], "Currents:", all_avg_mesures[2][1], "Power:", all_avg_mesures[2][2])
        print("Port:", all_avg_mesures[3][0], "Currents:", all_avg_mesures[3][1], "Power:", all_avg_mesures[3][2])
        print("Port:", all_avg_mesures[4][0], "Currents:", all_avg_mesures[4][1], "Power:", all_avg_mesures[4][2])
        print("Port:", all_avg_mesures[5][0], "Currents:", all_avg_mesures[5][1], "Power:", all_avg_mesures[5][2])
        print("Port:", all_avg_mesures[6][0], "Currents:", all_avg_mesures[6][1], "Power:", all_avg_mesures[6][2])
        print("Port:", all_avg_mesures[7][0], "Currents:", all_avg_mesures[7][1], "Power:", all_avg_mesures[7][2])

        #logging.info('Puissance moyenne: %s  Courant:%s ', a, b)


        #a = random.randrange(10)
        #b = random.randrange(50)
        #threading.Timer(10.0, self.logging_valeurs).start()
        #logging.info('Puissance moyenne: %s  Courant:%s ', a, b)
        #logging.info('Puissance moyenne: %s  Courant:%s  ADC0: %s  ADC1: %s', a, b,c,d)

    def get_avg_mesure(self):
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1, minutes=0)
        port_avg_data = []
        for i in range(8):
            port_data = self.repository.get_port_measures(i, start_time, end_time)
            mapper = MeasureMapper(*port_data, 3600, start_time, end_time)
            mapped_port_data = mapper.map_measures()
            port_avg_data.append((i, mapped_port_data[1], mapped_port_data[2]))
        print(port_avg_data)
        return port_avg_data


