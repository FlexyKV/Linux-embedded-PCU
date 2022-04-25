from datetime import datetime
from ..database_client.database_client import DatabaseClient



class RecordRepository:
    def __init__(self, db: DatabaseClient):
        self.db = db

    def get_port_records(self, port_id: int, start_time: datetime, end_time: datetime):
        with self.db as cur:
            port_data_query = """
            SELECT measure.current, measure.voltage, measure.power, record.record_datetime as "[timestamp]", 
            record.record_port_states FROM measure
            INNER JOIN record ON measure.record_id = record.id
            WHERE record.record_datetime >= ? AND record.record_datetime < ?
            AND measure.port_id = ?
            """
            cur.execute(port_data_query, [start_time, end_time, port_id])
            record_data = cur.fetchall()
        if not record_data:
            return -1
        return self.__extract_port_record_values(record_data, port_id)

    def get_instant_record(self):
        with self.db as cur:
            instant_data_query = """
            SELECT measure.current, measure.voltage, measure.power, record.record_datetime as "[timestamp]", 
            record.record_port_states, measure.port_id FROM measure
            INNER JOIN record ON measure.record_id = record.id
            WHERE record.id = (SELECT MAX(id) FROM record)
            """
            cur.execute(instant_data_query)
            record_data = cur.fetchall()
        if not record_data:
            return -1
        return self.__extract_instant_record_values(record_data)

    def __extract_instant_record_values(self, record_data: list):
        record_measures = list(map(lambda r_measure: (r_measure[0], r_measure[1], r_measure[2]), record_data))
        record_datetime = record_data[0][3]
        record_port_states = self.__bitmap_to_ports_state(record_data[0][4])

        return record_datetime, record_port_states, record_measures

    def __extract_port_record_values(self, record_data: list, port_id: int):
        record_measures = list(map(lambda r_measure: (r_measure[0], r_measure[1], r_measure[2]), record_data))
        record_datetime = list(map(lambda r_vo: r_vo[3], record_data))
        record_port_states = list(map(lambda ps: self.__bitmap_to_port_state(ps[4], port_id), record_data))

        return record_datetime, record_port_states, record_measures

    @staticmethod
    def __bitmap_to_port_state(bitmap: int, port_id: int):
        record_binary_states = [1 if digit == '1' else 0 for digit in bin(bitmap)[2:]]
        while len(record_binary_states) < 8:
            record_binary_states.insert(0, 0)
        return int(record_binary_states[port_id])

    @staticmethod
    def __bitmap_to_ports_state(bitmap: int):
        record_binary_states = [1 if digit == '1' else 0 for digit in bin(bitmap)[2:]]
        while len(record_binary_states) < 8:
            record_binary_states.insert(0, 0)
        return record_binary_states
