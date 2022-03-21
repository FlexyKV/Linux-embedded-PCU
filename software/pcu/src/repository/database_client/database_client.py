import sqlite3
from typing import Optional, Type
from types import TracebackType

DATABASE_PATH = r"/home/pi/pcu/sqlite_database/pcu_database.db"


class DatabaseClient:
    def open(self):
        self.conn = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
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
