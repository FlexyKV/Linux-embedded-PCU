import logging
import logging.handlers
from datetime import datetime, timedelta

NUM_PORTS = 8
SECONDS_PER_HOUR = 3600
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class SyslogLogger(object):
    def __init__(self, address, port, repo, map_measures):
        self.address = address
        self.port = port
        self.repository = repo
        self.map_measures = map_measures
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        syslog = logging.handlers.SysLogHandler(address=(self.address, int(self.port)))
        self.logger.addHandler(syslog)

    def log_values(self, hours):
        port_averages = self.get_avg_measures(hours)
        if not port_averages:
            return 0
        for port_id, avg, mx, mn, port_states in port_averages:
            states = [(dt.strftime(DATETIME_FORMAT), state) for dt, state in port_states]
            self.logger.info(
                f"Last {hours}h (Current, Voltage, Power);Port: {port_id}, "
                f"AVG: {avg}, MAX: {mx}, MIN:{mn}, Port states:{states}"
            )

    def get_avg_measures(self, hours):
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        port_avg_data = []
        for port_id in range(NUM_PORTS):
            port_data = self.repository.get_port_records(port_id, start_time, end_time)
            if port_data == -1:
                logging.info("No values for the last hour")
                return 0
            mapped = self.map_measures(*port_data, SECONDS_PER_HOUR)
            port_avg_data.append((port_id, mapped[1], mapped[2], mapped[3], mapped[4]))
        return port_avg_data
