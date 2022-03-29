import configparser
import enum
import sqlite3
from typing import Optional, Type
from types import TracebackType

PORT_DATABASE_TABLES = r"/home/pi/pcu/sqlite_database/port_database.sql"
PORT_DATABASE_PATH = r"/home/pi/pcu/sqlite_database/port_database.db"

RECORD_DATABASE_TABLES = r"/home/pi/pcu/sqlite_database/record_database.sql"
ROM_RECORD_DATABASE_PATH = r"/home/pi/pcu/sqlite_database/record_database.db"
RAM_RECORD_DATABASE_PATH = r"/var/tmp/record_database.db"

CONFIG_FILE_PATH = "/home/pi/pcu/src/config/config.ini"


class database_type(enum.Enum):
    port = 1
    record = 2


class memory_type(enum.Enum):
    rom = 1
    ram = 2


def get_record_memory_type():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    record_memory_type = memory_type[config["DATABASE"].get("record_memory_type")]
    return record_memory_type


class DatabaseClient:
    def __init__(self, database):
        self.disk_db_conn = None
        self.conn = None
        self.cur = None
        if database == database_type.port:
            self.db = PORT_DATABASE_PATH
            self.tables = PORT_DATABASE_TABLES
        elif database == database_type.record:
            if get_record_memory_type() == memory_type.rom:
                self.db = ROM_RECORD_DATABASE_PATH
            elif get_record_memory_type() == memory_type.ram:
                self.db = RAM_RECORD_DATABASE_PATH
            self.tables = RECORD_DATABASE_TABLES

    def initialise_db(self):
        with open(self.tables, 'r') as sql_file:
            sql_script = sql_file.read()
        self.open()
        try:
            self.cur.executescript(sql_script)
        except:
            pass
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
