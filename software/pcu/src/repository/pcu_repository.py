import sqlite3
from sqlite3 import Error
from datetime import timedelta, datetime


class PcuRepository:
    def __init__(self, db):
        self.db = db
        self.conn = None

    def open_connection(self):
        try:
            self.conn = sqlite3.connect(self.db, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        except Error as e:
            print(e)
            return -1
        return self.conn

    def close_connexion(self):
        self.conn.close()

    def __get_records(self, start_time: datetime, end_time: datetime):
        try:
            cur = self.conn.cursor()
            get_timeframe_query = """SELECT id, record_datetime as "[timestamp]", record_port_states FROM record 
            WHERE record_datetime >= ? AND record_datetime < ?"""
            cur.execute(get_timeframe_query, [start_time, end_time])
            records = cur.fetchall()
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        return records

    def __insert_record(self, record_datetime: datetime):
        try:
            cur = self.conn.cursor()
            get_states_query = """SELECT port_state FROM port"""
            cur.execute(get_states_query)
            port_states = list(map(lambda st: st[0], cur.fetchall()))
            int_state = 0
            for state in port_states:
                int_state = (int_state << 1) | state
            insert_record_query = """INSERT INTO record VALUES (NULL, ?, ?)"""
            cur.execute(insert_record_query, [record_datetime, int_state])
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        return cur.lastrowid

    def __get_measures(self, port_id: int, record_ids: list):
        try:
            cur = self.conn.cursor()
            get_measures = """SELECT measure.current, measure.voltage FROM measure WHERE record_id IN ({records})
             AND port_id = ?""".format(records=','.join(['?'] * len(record_ids)))
            query_args = record_ids + [port_id]
            cur.execute(get_measures, query_args)
            measures = cur.fetchall()
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        return measures

    def __insert_measure(self, record_id: int, port_id: int, current: float, voltage: float):
        try:
            cur = self.conn.cursor()
            get_port_query = """INSERT INTO measure VALUES (NULL, ?, ?, ?, ?)"""
            cur.execute(get_port_query, [record_id, port_id, current, voltage])
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        return cur.lastrowid

    def get_port_state(self, port_id: int):
        self.open_connection()
        try:
            cur = self.conn.cursor()
            get_port_query = """SELECT port_state FROM port WHERE id = ?"""
            cur.execute(get_port_query, [port_id])
            port_state = cur.fetchone()
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        self.close_connexion()
        if port_state is None:
            return port_state
        return port_state[0]

    def update_port_state(self, port_id: int, port_state: int):
        self.open_connection()
        try:
            cur = self.conn.cursor()
            get_port_query = """UPDATE port SET port_state = ? WHERE id = ?"""
            cur.execute(get_port_query, [port_state, port_id])
            get_port_query = """SELECT port_state FROM port WHERE id = ?"""
            cur.execute(get_port_query, [port_id])
            new_port_state = cur.fetchone()
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        self.close_connexion()
        return new_port_state[0]

    def insert_port_measures(self, record_datetime: datetime, current: list, voltage: list):

        self.open_connection()
        record_id = self.__insert_record(record_datetime)
        measure_ids = []
        for port_id in range(8):
            measure_ids.append(self.__insert_measure(record_id, port_id, current[port_id], voltage[port_id]))
        self.close_connexion()
        return measure_ids

    def get_port_measures(self, port_id: int, start_time: datetime, end_time: datetime):

        self.open_connection()

        # when big number of record i get 1 more record id then record datetime, WTF WHY?
        records = self.__get_records(start_time, end_time)
        record_ids = list(map(lambda r_id: r_id[0], records))
        record_datetime = list(map(lambda dt: dt[1], records))
        record_ports_states = list(map(lambda st: st[2], records))
        record_port_states = []

        # get port state from list of states
        for record_states in record_ports_states:
            record_binary_states = [1 if digit == '1' else 0 for digit in bin(record_states)[2:]]
            while len(record_binary_states) < 8:
                record_binary_states.insert(0, 0)
            port_id_record_state = int(record_binary_states[port_id])
            record_port_states.append(port_id_record_state)

        measures = self.__get_measures(port_id, record_ids)
        self.close_connexion()

        if not records:
            return -1

        return record_datetime, record_port_states, measures


    def create_ports(self):
        if self.get_port_state(2) is None:
            self.open_connection()
            try:
                new_port_query = "INSERT INTO port VALUES (?, 0)"
                for port in range(8):
                    cur = self.conn.cursor()
                    cur.execute(new_port_query, [port])
                self.conn.commit()
            except Error as e:
                print(e)
                return -1
        self.close_connexion()
        return 0

    def create_tables(self):
        """create tables"""

        self.open_connection()

        sql_create_record = """CREATE TABLE IF NOT EXISTS "record" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "record_datetime" DATETIME NOT NULL,
        "record_port_states" INTEGER NOT NULL
        );"""

        sql_create_port = """CREATE TABLE IF NOT EXISTS "port" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "port_state" INTEGER NOT NULL
        );"""

        sql_create_measure = """ CREATE TABLE IF NOT EXISTS "measure" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "record_id" INTEGER NOT NULL,
        "port_id" INTEGER NOT NULL,
        "current" REAL NOT NULL,
        "voltage" REAL NOT NULL,
        FOREIGN KEY ("record_id") REFERENCES "record" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY ("port_id") REFERENCES "port" ("id") ON DELETE CASCADE ON UPDATE CASCADE
        );"""

        try:
            cur = self.conn.cursor()
            cur.execute(sql_create_record)
            cur.execute(sql_create_port)
            cur.execute(sql_create_measure)
            self.conn.commit()
        except Error as e:
            print(e)
            return -1

        self.close_connexion()
        return 0
