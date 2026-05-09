import configparser
import time

from log.syslog_logger import SyslogLogger
from repository.database_client.database_client import (
    CONFIG_FILE_PATH,
    DatabaseClient,
    database_type,
)
from repository.record.mapper.mapper import map_measures
from repository.record.record_repository import RecordRepository

SECONDS_PER_HOUR = 3600
DAILY_REPORT_HOURS = 24


def get_log_server_endpoint():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    app = config["APP"]
    return app.get("log_server_ip"), app.get("log_server_port")


log_ip, log_port = get_log_server_endpoint()
db_client = DatabaseClient(database_type.record)
pcu_logging_repo = RecordRepository(db_client)
pcu_logging = SyslogLogger(log_ip, log_port, pcu_logging_repo, map_measures)

hours = 0
start_time = time.time()

while True:
    if (time.time() - start_time) < SECONDS_PER_HOUR:
        time.sleep(1)
        continue
    start_time = time.time()
    pcu_logging.log_values(1)
    hours += 1
    if hours >= DAILY_REPORT_HOURS:
        pcu_logging.log_values(DAILY_REPORT_HOURS)
        hours = 0
