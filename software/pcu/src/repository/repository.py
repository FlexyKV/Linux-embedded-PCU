import sqlite3
from sqlite3 import Error

db_file_path = r"pythonsqlitetest.db"

select_command = "SELECT * FROM {table}"
insert_command = "INSERT INTO {table} VALUES ({values})"
update_all_command = "UPDATE {table} set {values}"
update_id_command = "UPDATE {table} set {values} where id={id}"
delete_all_command = "DELETE FROM {table}"
delete_id_command = "DELETE FROM {table} WHERE id={id}"


class Repository:
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.conn = None

    def create_connexion(self):
        try:
            self.conn = sqlite3.connect(self.dbfile)
        except Error as e:
            print(e)
            return False
        return self.conn

    def select(self, table):
        try:
            c = self.conn.cursor()
            c.execute(select_command.format(table=table))
            rows = c.fetchall()
        except Error as e:
            print(e)
            return -1
        return rows

    def insert(self, table, list_values: list):
        insert_values = ""
        for value in list_values:
            if isinstance(value, str) and value != "NULL":
                insert_values += "\"" + value + "\"" + ", "
            else:
                insert_values += str(value) + ", "
        insert_values = insert_values[:-2]
        try:
            c = self.conn.cursor()
            c.execute(insert_command.format(table=table, values=insert_values))
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        return c.lastrowid

    def update_all(self, table, dict_values: dict):
        insert_values = ""
        for key, value in dict_values.items():
            if isinstance(value, str) and value != "NULL":
                insert_values += key + " = " + "\"" + value + "\"" + ", "
            else:
                insert_values += key + " = " + str(value) + ", "
        insert_values = insert_values[:-2]
        try:
            c = self.conn.cursor()
            c.execute(update_all_command.format(
                table=table, values=insert_values))
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        return c.lastrowid

    def update_id(self, table, values: dict, id):
        insert_values = ""
        for key, value in values.items():
            if isinstance(value, str) and value != "NULL":
                insert_values += key + " = " + "\"" + value + "\"" + ", "
            else:
                insert_values += key + " = " + str(value) + ", "
        insert_values = insert_values[:-2]
        try:
            c = self.conn.cursor()
            c.execute(insert_command.format(
                table=table, values=insert_values, id=id))
            self.conn.commit()
        except Error as e:
            print(e)
            return -1
        return c.lastrowid

    def delete_all(self, table):
        try:
            c = self.conn.cursor()
            c.execute(delete_all_command.format(table=table))
            self.conn.commit()
        except Error as e:
            print(e)
            return False
        return True

    def delete_id(self, table, id):
        try:
            c = self.conn.cursor()
            c.execute(delete_id_command.format(table=table, id=id))
            self.conn.commit()
        except Error as e:
            print(e)
            return False
        return True


def create_table(connection):
    """create tables"""

    sql_create_record = """CREATE TABLE "record" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "start" DATETIME NOT NULL,
    "end" DATETIME NOT NULL,
    "period" INTEGER NOT NULL
    );"""

    sql_create_port = """CREATE TABLE "port" (
       "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
       "port_number" INTEGER NOT NULL,
       "port_state" INTEGER NOT NULL
       );"""

    sql_create_measure = """ CREATE TABLE "measures" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
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
    except Error as e:
        print(e)


if __name__ == '__main__':

    #test working
    repo = Repository(db_file_path)
    conn = repo.create_connexion()
    if not conn:
        print("database connexion error")
    create_table(conn)

    # manual insert
    #insert_command = """INSERT INTO port (id, port_number, port_state) VALUES (NULL, 5, 1);"""
    #cur = conn.cursor()
    # cur.execute(insert_command)
    # conn.commit()

    # function insert
    repo.insert("port", ["NULL", 6, 0])

