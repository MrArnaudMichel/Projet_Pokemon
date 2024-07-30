import sqlite3


class SQL:
    def __init__(self):
        """
        Initialize the SQL connection
        """
        self.connection = sqlite3.connect("../../assets/base.db")
        self.cursor = self.connection.cursor()

    def get_connection(self):
        """
        Get the connection
        :return:
        """
        return self.connection

    def get_cursor(self):
        """
        Get the cursor
        :return:
        """
        return self.cursor

    def select(self, table: str, columns: list[str], where: str = None, order: str = None, limit: int = None) -> list[
        tuple]:
        """
        Select data from the database
        :param table:
        :param columns:
        :param where:
        :param order:
        :param limit:
        :return:
        """
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

    def get_name_map(self, map_id: str) -> str:
        """
        Get the name of the map
        :param map_id:
        :return:
        """
        try:
            return self.select("map_name", ["fr"], f"id = '{map_id}'")[0][0]
        except IndexError:
            return "error"
