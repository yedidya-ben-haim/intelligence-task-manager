import mysql.connector


class ConnectionDB:
    def __init__(self):
        self.user = 'root'
        self.password = '1234'
        self.host = '127.0.0.1'
        self.database = 'Intelligence_db'

    def get_connection(self):
        return mysql.connector.connect(user=self.user, password=self.password,
                              host=self.host,
                              database=self.database)


