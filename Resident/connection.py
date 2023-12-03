import mysql.connector

class DatabaseConnector:
    def __init__(self):
        self._connection = self._create_connection()

    def _create_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="barangay"
        )

    def get_connection(self):
        return self._connection

# Create an instance of DatabaseConnector
db_connector = DatabaseConnector()

# Use the connection in your application
connection = db_connector.get_connection()

# If you need to reset the connection, recreate the instance
db_connector = DatabaseConnector()
