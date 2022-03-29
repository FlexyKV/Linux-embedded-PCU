# myapp.py
import logging
import logging.handlers
from datetime import datetime, timedelta
from src.repository.record.mapper.mapper import map_measures


class loggingSyslog(object):

    def __init__(self, address, port, repo):
        self.address = address
        self.port = port
        self.repository = repo

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        syslog = logging.handlers.SysLogHandler(address=(self.address, self.port))
        logger.addHandler(syslog)

    def logging_valeurs(self):
        all_avg_mesures = self.get_avg_mesure()
        for i in range(8):
            #logging.info("Port:" , all_avg_mesures[i][0], "Power avg:", (all_avg_mesures[i][1].pop() * all_avg_mesures[i][2].pop()) )
            print("Port:", all_avg_mesures[i][0],
                         "Power avg:",(all_avg_mesures[i][1].pop() * all_avg_mesures[i][2].pop()),"W")

        #threading.Timer(10.0, self.logging_valeurs).start()


    def get_avg_mesure(self):
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1, minutes=0)
        port_avg_data = []
        for i in range(8):
            port_data = self.repository.get_port_measures(i, start_time, end_time)
            #If no data
            if port_data == -1:
                logging.info("Aucune valeur pour la dernière heure")
                return 0
            else:
                mapped_port_data = map_measures(*port_data, 3600)
                port_avg_data.append((i, mapped_port_data[1], mapped_port_data[2]))
        #print(port_avg_data)
        return port_avg_data


