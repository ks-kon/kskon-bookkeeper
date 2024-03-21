import sqlite3

class DatabaseConnection:
    def __init__(self, db_name='bookkeeper.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        if params is not None:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()

    # def insert_into(self, query, params=None):

    def close_connection(self):
        self.conn.close()