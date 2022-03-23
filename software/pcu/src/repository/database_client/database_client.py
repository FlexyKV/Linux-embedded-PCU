import sqlite3
from typing import Optional, Type
from types import TracebackType

PORT_DATABASE_PATH = r"/home/pi/pcu/sqlite_database/port_database.db"
RECORD_DATABASE_PATH = r"/home/pi/pcu/sqlite_database/record_database.db"


class DatabaseClient:
    def __init__(self, database):
        self.disk_db_conn = None
        self.conn = None
        self.cur = None
        if database == "port":
            self.db = PORT_DATABASE_PATH
            self.tables = r"/home/pi/pcu/sqlite_database/port_database.sql"
        elif database == "record":
            self.db = RECORD_DATABASE_PATH  # TODO ifelse for in RAM
            self.tables = r"/home/pi/pcu/sqlite_database/record_database.sql"

    def initialise_db(self):
        with open(self.tables, 'r') as sql_file:
            sql_script = sql_file.read()
        self.open()
        self.cur.executescript(sql_script)
        self.close()

    def open(self):
        self.conn = sqlite3.connect(self.db, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def __enter__(self):
        self.open()
        self.__enable_foreign_keys()
        return self.cur

    def __exit__(self, exctype: Optional[Type[BaseException]], excinst: Optional[BaseException],
                 exctb: Optional[TracebackType]):
        if exctype is not None:
            self.conn.rollback()
            self.conn.close()
        else:
            self.close()

    def __enable_foreign_keys(self):
        query = """
        PRAGMA foreign_keys=ON
        """
        self.cur.execute(query)
