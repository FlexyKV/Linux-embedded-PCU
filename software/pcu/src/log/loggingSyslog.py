# myapp.py
import logging
import logging.handlers
from datetime import datetime, timedelta


class loggingSyslog(object):

    def __init__(self, address, port, repo, map_measures):
        self.address = address
        self.port = port
        self.repository = repo
        self.map_measures = map_measures
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        print((self.address, int(self.port)))
        syslog = logging.handlers.SysLogHandler(address=(self.address, int(self.port)))
        self.logger.addHandler(syslog)

    def log_values(self, hours):
        all_avg_mesures = self.get_avg_mesure(hours)
        if not all_avg_mesures:
            return 0
        for i in range(8):
            port_states = list(map(lambda dt: (dt[0].strftime('%Y-%m-%dT%H:%M:%S.%fZ'), dt[1]), all_avg_mesures[i][4]))

            self.logger.info("Last " + str(hours) + "h (Current, Voltage, Power);" + "Port: " + str(i) + ", AVG: " + str(all_avg_mesures[i][1]) +
                             ", MAX: " + str(all_avg_mesures[i][2]) + ", MIN:" + str(all_avg_mesures[i][3]) +
                         ", Port states:" + str(port_states))

    def get_avg_mesure(self, hours):
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours, minutes=0)
        port_avg_data = []
        for i in range(8):
            port_data = self.repository.get_port_records(i, start_time, end_time)
            #If no data
            if port_data == -1:
                logging.info("Aucune valeur pour la dernière heure")
                return 0
            else:
                mapped_port_data = self.map_measures(*port_data, 3600)
                port_avg_data.append((i, mapped_port_data[1], mapped_port_data[2], mapped_port_data[3], mapped_port_data[4]))
        return port_avg_data


