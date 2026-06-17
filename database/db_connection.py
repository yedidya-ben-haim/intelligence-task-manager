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
            print(f"An error occurred while connecting to the database {e}.")
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
            cursor.close()
            conn.close()
            print(f"An error occurred while creating the database {e}.")
            return None


    def create_tables(self):
        """
            Creates both tables if they do not exist
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        agents_table_query = """CREATE TABLE IF NOT EXISTS agents (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(50) NOT NULL,
                                specialty VARCHAR(50) NOT NULL,
                                is_active BOOLEAN DEFAULT TRUE,
                                completed_missions INT DEFAULT 0,
                                failed_missions INT DEFAULT 0,
                                agent_rank ENUM('Junior', 'Senior', 'Commander')
                                );
                        """

        # todo: difficulty, importance INT 1-10

        missions_table_query = """CREATE TABLE IF NOT EXISTS missions (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    title VARCHAR(50) NOT NULL,
                                    description TEXT NOT NULL,
                                    location VARCHAR(100) NOT NULL,
                                    difficulty INT NOT NULL,
                                    importance INT NOT NULL,
                                    status VARCHAR(50) DEFAULT 'NEW',
                                    risk_level VARCHAR(50) NOT NULL,
                                    assigned_agent_id INT DEFAULT NULL
                                    );
                                """

        try:
            cursor.execute(agents_table_query)
            cursor.execute(missions_table_query)

            cursor.close()
            conn.close()


        except Exception as e:
            cursor.close()
            conn.close()
            print(f"An error occurred while creating the tables {e}.")






