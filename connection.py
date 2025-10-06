import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, host="localhost", user="ITS_2025", password="ITS_2025", database="password_manager"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def open(self):
        """Opens the connection to the database"""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                print("Connection established successfully!")
        except Error as e:
            print("Connection error:", e)

    def execute_query(self, query, params=None):
        """Executes an SQL query"""
        if self.conn is None or not self.conn.is_connected():
            print("Connection is not active.")
            return None
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print("Error while executing query:", e)
            return None

    def close(self):
        """Closes the connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Connection closed.")