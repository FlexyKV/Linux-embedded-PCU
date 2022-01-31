import sqlite3
from sqlite3 import Error
import datetime

db_file_path = r"pythonsqlitetest.db"


class PcuRepository:
    def __init__(self, db):
        self.db = db
        self.conn = None

    def open_connection(self):
        try:
            self.conn = sqlite3.connect(self.db)
        except Error as e:
            print(e)
            return False
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
            get_measures = """SELECT measure.current, voltage FROM measure WHERE record_id IN ({records})
             AND port_id = ?""".format(records=','.join(['?'] * len(record_ids)))
            query_args = record_ids.append(port_id)
            cur.execute(get_measures, query_args)
            measures = cur.fetchall()
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        return measures

    def __insert_measure(self, port_id: int, record_id: int, current: float, voltage: float):
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
        self.conn = self.open_connection()
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
        return port_state

    def update_port_state(self, port_id: int, port_state: int):
        self.conn = self.open_connection()
        try:
            cur = self.conn.cursor()
            get_port_query = """UPDATE port SET port_state = ? WHERE id = ?"""
            cur.execute(get_port_query, [port_state, port_id])
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        self.close_connexion()
        return port_id

    def insert_port_measure(self, port_id: int, record_datetime: datetime, record_period: int,
                            current: float, voltage: float):
        self.conn = self.open_connection()

        record_id = self.__insert_record(record_datetime, record_period)

        measure_id = self.__insert_measure(record_id, port_id, current, voltage)

        self.close_connexion()
        return measure_id

    def get_port_measures(self, port_id: int, start_time: datetime, end_time: datetime, period: int):
        self.conn = self.open_connection()

        record_ids = self.__get_period_record_ids(start_time, end_time, period)

        measures = self.__get_measures(port_id, record_ids)

        self.close_connexion()
        return measures


def create_table(connection):
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
        c = connection.cursor()
        c.execute(sql_create_record)
        c.execute(sql_create_port)
        c.execute(sql_create_measure)
        conn.commit()
    except Error as e:
        print(e)


if __name__ == '__main__':

    # initialise database
    repo = PcuRepository(db_file_path)
    conn = repo.open_connection()
    if not conn:
        print("database connexion error")

    # create tables if they don't exist
    create_table(conn)

    # create ports if they don't exist
    if repo.get_port_state(0) is None:
        new_port_query = "INSERT INTO port VALUES (?, 0)"
        for port in range(8):
            cursor = conn.cursor()
            cursor.execute(new_port_query, [port])
        conn.commit()
    conn.close()
