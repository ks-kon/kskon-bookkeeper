"""
взаимодействие с датабазой
"""

import sqlite3


class DatabaseConnection:
    """
    взаимодействие с датабазой
    """
    def __init__(self, db_name: str = 'bookkeeper.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute_query(self, query: str, params: str | None = None) -> list[()] | None:
        """
        выполнение запроса
        """
        if params is not None:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()

    def close_connection(self) -> None:
        """
        закрытие соединения
        """
        self.conn.close()
