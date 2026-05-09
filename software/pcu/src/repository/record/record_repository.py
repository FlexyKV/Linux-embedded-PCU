from datetime import datetime

from ..database_client.database_client import DatabaseClient

NUM_PORTS = 8


def _bitmap_to_ports_state(bitmap: int):
    return [int(d) for d in bin(bitmap)[2:].zfill(NUM_PORTS)]


class RecordRepository:
    def __init__(self, db: DatabaseClient):
        self.db = db

    def get_port_records(self, port_id: int, start_time: datetime, end_time: datetime):
        """Return record data for port_id between start_time and end_time."""
        with self.db as cur:
            query = """
            SELECT measure.current, measure.voltage, measure.power,
                   record.record_datetime as "[timestamp]", record.record_port_states
            FROM measure
            INNER JOIN record ON measure.record_id = record.id
            WHERE record.record_datetime >= ? AND record.record_datetime < ?
              AND measure.port_id = ?
            """
            cur.execute(query, [start_time, end_time, port_id])
            record_data = cur.fetchall()
        if not record_data:
            return -1
        return self.__extract_port_record_values(record_data, port_id)

    def get_instant_record(self):
        """Return the latest record + port state for all ports."""
        with self.db as cur:
            query = """
            SELECT measure.current, measure.voltage, measure.power,
                   record.record_datetime as "[timestamp]",
                   record.record_port_states, measure.port_id
            FROM measure
            INNER JOIN record ON measure.record_id = record.id
            WHERE record.id = (SELECT MAX(id) FROM record)
            """
            cur.execute(query)
            record_data = cur.fetchall()
        if not record_data:
            return -1
        return self.__extract_instant_record_values(record_data)

    @staticmethod
    def __extract_instant_record_values(record_data: list):
        record_measures = [(r[0], r[1], r[2]) for r in record_data]
        record_datetime = record_data[0][3]
        record_port_states = _bitmap_to_ports_state(record_data[0][4])
        return record_datetime, record_port_states, record_measures

    @staticmethod
    def __extract_port_record_values(record_data: list, port_id: int):
        record_measures = [(r[0], r[1], r[2]) for r in record_data]
        record_datetime = [r[3] for r in record_data]
        record_port_states = [_bitmap_to_ports_state(r[4])[port_id] for r in record_data]
        return record_datetime, record_port_states, record_measures
