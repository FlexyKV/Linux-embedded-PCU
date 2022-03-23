from sqlite3 import Cursor
from datetime import datetime
from ..database_client.database_client import DatabaseClient


# TODO change port state bitmap to port state in measures
class AdcRepository:
    def __init__(self, db: DatabaseClient):
        self.db = db

    def insert_port_measures(self, record_datetime: datetime, current: list, voltage: list):
        with self.db as cur:
            record_id = self.__insert_record(cur, record_datetime)
            measure_ids = []
            for port_id in range(8):
                measure_ids.append(self.__insert_measure(cur, record_id, port_id, current[port_id], voltage[port_id]))
        return measure_ids

    @staticmethod
    def __insert_record(cur: Cursor, record_datetime: datetime):
        get_states_query = """SELECT port_state FROM port"""
        cur.execute(get_states_query)
        port_states = list(map(lambda st: st[0], cur.fetchall()))
        int_state = 0
        for state in port_states:
            int_state = (int_state << 1) | state
        insert_record_query = """INSERT INTO record VALUES (NULL, ?, ?)"""
        cur.execute(insert_record_query, [record_datetime, int_state])
        return cur.lastrowid

    @staticmethod
    def __insert_measure(cur: Cursor, record_id: int, port_id: int, current: float, voltage: float):
        get_port_query = """INSERT INTO measure VALUES (NULL, ?, ?, ?, ?)"""
        cur.execute(get_port_query, [record_id, port_id, current, voltage])
        return cur.lastrowid



