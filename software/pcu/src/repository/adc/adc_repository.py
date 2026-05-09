from datetime import datetime
from sqlite3 import Cursor

from ..database_client.database_client import DatabaseClient

NUM_PORTS = 8


class AdcRepository:
    def __init__(self, record_db: DatabaseClient, port_db: DatabaseClient):
        self.record_db = record_db
        self.port_db = port_db

    def insert_port_measures(
        self, record_datetime: datetime, current: list, voltage: float, power: list
    ):
        """Insert one record + per-port measures, snapshotting current port states."""
        with self.port_db as port_cur:
            port_states = self.__get_port_states(port_cur)
        with self.record_db as record_cur:
            record_id = self.__insert_record(record_cur, record_datetime, port_states)
            measure_ids = [
                self.__insert_measure(record_cur, record_id, port_id, current[port_id], voltage, power[port_id])
                for port_id in range(NUM_PORTS)
            ]
        return measure_ids

    @staticmethod
    def __get_port_states(cur: Cursor):
        cur.execute("SELECT port_state FROM port")
        return [row[0] for row in cur.fetchall()]

    @staticmethod
    def __insert_record(cur: Cursor, record_datetime: datetime, port_states: list):
        bitmap = 0
        for state in port_states:
            bitmap = (bitmap << 1) | state
        cur.execute("INSERT INTO record VALUES (NULL, ?, ?)", [record_datetime, bitmap])
        return cur.lastrowid

    @staticmethod
    def __insert_measure(
        cur: Cursor, record_id: int, port_id: int, current: float, voltage: float, power: float
    ):
        cur.execute(
            "INSERT INTO measure VALUES (NULL, ?, ?, ?, ?, ?)",
            [record_id, port_id, current, voltage, power],
        )
        return cur.lastrowid
