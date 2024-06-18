import sqlite3


class SQL:
    def __init__(self):
        self.connection = sqlite3.connect("../../assets/base.db")
        self.cursor = self.connection.cursor()

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor

    def select(self, table: str, columns: list[str], where: str = None, order: str = None, limit: int = None) -> list[
        tuple]:
        query: str = f"SELECT {'. '.join(columns)} FROM {table}"
        if where:
            query += f" WHERE {where}"
        if order:
            query += f" ORDER BY {order}"
        if limit:
            query += f" LIMIT {limit}"
        print(query)
        self.cursor.execute(query)
        return self.cursor.fetchall()
