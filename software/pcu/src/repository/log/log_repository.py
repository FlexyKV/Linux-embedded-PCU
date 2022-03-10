from datetime import datetime, timedelta
from src.repository.database_client.database_client import DatabaseClient


class LogRepository:
    def __init__(self, db: DatabaseClient):
        self.db = db

    def get_last_hour_record(self):
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1, minutes=0)
        port_records = []
        with self.db as cur:
            for port_id in range(8):
                port_data_query = """
                SELECT measure.current, measure.voltage, record.record_datetime as "[timestamp]", 
                record.record_port_states FROM measure
                INNER JOIN record ON measure.record_id = record.id
                WHERE record.record_datetime >= ? AND record.record_datetime < ?
                AND measure.port_id = ?
                                   """
                cur.execute(port_data_query, [start_time, end_time, port_id])
            record_data = cur.fetchall()
            port_records.append(record_data)
        return port_records  # TODO map data

    def get_last_day_record(self):
        end_time = datetime.now()
        start_time = end_time - timedelta(days=1, hours=0, minutes=0)
        port_records = []
        with self.db as cur:
            for port_id in range(8):
                port_data_query = """
                SELECT measure.current, measure.voltage, record.record_datetime as "[timestamp]", 
                record.record_port_states FROM measure
                INNER JOIN record ON measure.record_id = record.id
                WHERE record.record_datetime >= ? AND record.record_datetime < ?
                AND measure.port_id = ?
                                   """
                cur.execute(port_data_query, [start_time, end_time, port_id])
            record_data = cur.fetchall()
            port_records.append(record_data)
        return port_records  # TODO map data

    def get_port_measures(self, port_id: int, start_time: datetime, end_time: datetime):
        with self.db as cur:
            port_data_query = """
            SELECT measure.current, measure.voltage, record.record_datetime as "[timestamp]", 
            record.record_port_states FROM measure
            INNER JOIN record ON measure.record_id = record.id
            WHERE record.record_datetime >= ? AND record.record_datetime < ?
            AND measure.port_id = ?
                               """
            cur.execute(port_data_query, [start_time, end_time, port_id])
            record_data = cur.fetchall()
        if not record_data:
            return -1

        return self.__extract_record_values(record_data, port_id)

    def __extract_record_values(self, record_data: list, port_id: int):
        record_measures = list(map(lambda r_measure: (r_measure[0], r_measure[1]), record_data))
        record_datetime = list(map(lambda r_vo: r_vo[2], record_data))
        record_port_states = list(map(lambda ps: self.__bitmap_to_port_state(ps[3], port_id), record_data))

        return record_datetime, record_port_states, record_measures



