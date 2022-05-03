from ..database_client.database_client import DatabaseClient


class PortsRepository:
    def __init__(self, db: DatabaseClient):
        self.db = db

    def get_port_state(self, port_id: int):
        """ get port state from database """
        with self.db as cur:
            get_port_query = """SELECT port_state FROM port WHERE id = ?"""
            cur.execute(get_port_query, [port_id])
            port_state = cur.fetchone()
        if port_state is None:
            return port_state
        return port_state[0]

    def update_port_state(self, port_id: int, port_state: int):
        """ update port state in database """
        with self.db as cur:
            put_port_query = """UPDATE port SET port_state = ? WHERE id = ?"""
            cur.execute(put_port_query, [port_state, port_id])
            get_port_query = """SELECT port_state FROM port WHERE id = ?"""
            cur.execute(get_port_query, [port_id])
            new_port_state = cur.fetchone()
        return new_port_state[0]
