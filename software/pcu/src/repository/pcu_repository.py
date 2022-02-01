import sqlite3
from sqlite3 import Error
import datetime


class PcuRepository:
    def __init__(self, db):
        self.db = db
        self.conn = None

    def open_connection(self):
        try:
            self.conn = sqlite3.connect(self.db)
            self.conn.row_factory = lambda cursor, row: row[0] #TODO change this system
        except Error as e:
            print(e)
            return -1
        return self.conn

    def close_connexion(self):
        self.conn.close()

    def __get_record_id(self, record_datetime: datetime, record_period: int):
        try:
            cur = self.conn.cursor()
            get_timeframe_query = """SELECT id FROM record WHERE record_datetime = ? AND record_period = ?"""
            cur.execute(get_timeframe_query, [record_datetime, record_period])
            record_id = cur.fetchone()
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        return record_id

    def __get_period_record_ids(self, start_time: datetime, end_time: datetime, record_period: int):
        try:
            cur = self.conn.cursor()
            get_timeframe_query = """SELECT id FROM record WHERE record_datetime >= ? AND record_datetime < ? 
            AND record_period = ?"""
            cur.execute(get_timeframe_query, [start_time, end_time, record_period])
            record_ids = cur.fetchall()
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        return record_ids

    def __insert_record(self, record_datetime: datetime, period: int):
        try:
            cur = self.conn.cursor()
            insert_record_query = """INSERT INTO record VALUES (NULL, ?, ?)"""
            cur.execute(insert_record_query, [record_datetime, period])
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
        try:
            cur = self.conn.cursor()
            get_port_query = """SELECT port_state FROM port WHERE id = ?"""
            cur.execute(get_port_query, [port_id])
            port_state = cur.fetchone()
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        return port_state

    def update_port_state(self, port_id: int, port_state: int):
        try:
            cur = self.conn.cursor()
            get_port_query = """UPDATE port SET port_state = ? WHERE id = ?"""
            cur.execute(get_port_query, [port_state, port_id])
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        return port_id

    def insert_port_measures(self, record_datetime: datetime, record_period: int,
                             current: list, voltage: list):

        record_id = self.__insert_record(record_datetime, record_period)
        measure_ids = []
        for port_id in range(8):
            measure_ids.append(self.__insert_measure(record_id, port_id, current[port_id], voltage[port_id]))

        return measure_ids

    def get_port_measures(self, port_id: int, start_time: datetime, end_time: datetime, period: int):

        record_ids = self.__get_period_record_ids(start_time, end_time, period)

        measures = self.__get_measures(port_id, record_ids)

        return measures

    def create_ports(self):
        if self.get_port_state(2) is None:
            try:
                new_port_query = "INSERT INTO port VALUES (?, 0)"
                for port in range(8):
                    cur = self.conn.cursor()
                    cur.execute(new_port_query, [port])
                self.conn.commit()
            except Error as e:
                print(e)
                return -1

    def create_tables(self):
        """create tables"""

        sql_create_record = """CREATE TABLE IF NOT EXISTS "record" (
        "id" INTEGER NOT NULL PRIMARY KEY,
        "record_datetime" DATETIME NOT NULL,
        "record_period" INTEGER NOT NULL
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

