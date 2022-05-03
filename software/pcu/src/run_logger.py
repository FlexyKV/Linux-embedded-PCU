import configparser
import time
from log.loggingSyslog import loggingSyslog
from repository.record.record_repository import RecordRepository
from repository.database_client.database_client import DatabaseClient, CONFIG_FILE_PATH, database_type
from repository.record.mapper.mapper import map_measures


def get_log_server_ip():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    log_server_ip = config["APP"].get("log_server_ip")
    return log_server_ip


def get_log_server_port():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    log_server_port = config["APP"].get("log_server_port")
    return log_server_port


db_client = DatabaseClient(database_type.record)
pcu_logging_repo = RecordRepository(db_client)
pcu_logging = loggingSyslog(get_log_server_ip(), get_log_server_port(), pcu_logging_repo, map_measures)

hours = 0
start_time = time.time()

while True:
    if (time.time() - start_time) < 3600:  # 3600 second for hour
        time.sleep(1)
        continue
    start_time = time.time()
    pcu_logging.log_values(1)
    hours += 1
    if hours >= 24:
        pcu_logging.log_values(24)
        hours = 0




