from sqlite3 import Cursor
from datetime import datetime
from ..database_client.database_client import DatabaseClient


# TODO change port state bitmap to port state in measures
class AdcRepository:
    def __init__(self, record_db: DatabaseClient, port_db: DatabaseClient):
        self.record_db = record_db
        self.port_db = port_db

    def insert_port_measures(self, record_datetime: datetime, current: list, voltage: int, power: list):
        """ insert port measures and state in database"""
        with self.port_db as port_cur:
            port_states = self.__get_port_states(port_cur)
        with self.record_db as record_cur:
            record_id = self.__insert_record(record_cur, record_datetime, port_states)
            measure_ids = []
            for port_id in range(8):
                measure_ids.append(self.__insert_measure(record_cur, record_id, port_id, current[port_id], voltage,
                                                         power[port_id]))
        return measure_ids

    @staticmethod
    def __get_port_states(cur: Cursor):
        get_states_query = """SELECT port_state FROM port"""
        cur.execute(get_states_query)
        port_states = list(map(lambda st: st[0], cur.fetchall()))
        return port_states

    @staticmethod
    def __insert_record(cur: Cursor, record_datetime: datetime, port_states: list):
        int_state = 0
        for state in port_states:
            int_state = (int_state << 1) | state
        insert_record_query = """INSERT INTO record VALUES (NULL, ?, ?)"""
        cur.execute(insert_record_query, [record_datetime, int_state])
        return cur.lastrowid

    @staticmethod
    def __insert_measure(cur: Cursor, record_id: int, port_id: int, current: float, voltage: float, power: float):
        set_measure_query = """INSERT INTO measure VALUES (NULL, ?, ?, ?, ?, ?)"""
        cur.execute(set_measure_query, [record_id, port_id, current, voltage, power])
        return cur.lastrowid


