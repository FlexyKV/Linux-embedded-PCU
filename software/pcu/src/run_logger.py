from src.log.loggingSyslog import loggingSyslog
from src.repository.record.record_repository import RecordRepository
from src.repository.database_client.database_client import DatabaseClient

db_client = DatabaseClient()
pcu_logging_repo = RecordRepository(db_client)
pcu_logging = loggingSyslog("192.168.1.80", 514, pcu_logging_repo)
pcu_logging.logging_valeurs()
