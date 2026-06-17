import mysql.connector


class ConnectionDB:
    """
        Responsible for connecting to the MySQL container, creating the database, and creating the tables.
    """
    def __init__(self):
        self.user = 'root'
        self.password = '1234'
        self.host = '127.0.0.1'
        self.database = 'Intelligence_db'

    def get_connection(self):
        """
            Returns an active connection to MySQL
        """
        try:
            return mysql.connector.connect(user=self.user, password=self.password,
                              host=self.host,
                              database=self.database)
        except Exception as e:
            return None


    def create_database(self):
        """
            Creates Intelligence_db if it does not exist
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        query = """CREATE DATABASE IF NOT EXISTS Intelligence_db"""

        try:
            cursor.execute(query)

            cursor.close()
            conn.close()

        except Exception as e:
            return None



new_db = ConnectionDB()
new_db.create_database()




