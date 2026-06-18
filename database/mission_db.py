from db_connection import ConnectionDB
from agent_db import AgentDB


class Mission:
    def __init__(self, title, description, location, difficulty, importance, status, risk_level, assigned_agent_id):
        self.title = title
        self.description = description
        self.location = location
        self.difficulty = difficulty
        self.importance = importance
        self.status = status
        self.risk_level = risk_level
        self.assigned_agent_id = assigned_agent_id


class MissionDB:
    """
        Responsible for managing the mission table including creating mission objects.
    """

    def __init__(self):
        self.conn = ConnectionDB().get_connection()
        self.agent_db = AgentDB()


    def create_mission(self, data: dict):
        """
            Creates a new mission and returns the mission object.
        """
        cursor = self.conn.cursor()

        # Calculating risk_level
        difficulty = data.get("difficulty", 1)
        importance = data.get("importance", 1)
        risk_score = difficulty * 2 + importance

        if risk_score <= 9:
            risk_level = "LOW"
        elif risk_score <= 17:
            risk_level = "MEDIUM"
        elif risk_score <= 24:
            risk_level = "HIGH"
        elif 24 <= risk_score:
            risk_level = "CRITICAL"


        value = (data["title"], data["description"], data["location"], data["difficulty"], data["importance"],
                 data["status"], risk_level, data["assigned_agent_id"])

        query = """insert into missions (title, description, location, difficulty, importance, status, risk_level, assigned_agent_id)
                                values (%s, %s, %s, %s, %s, %s, %s, %s);
                """

        try:
            cursor.execute(query, value)
            self.conn.commit()

            new_agent = Mission(data["title"], data["description"], data["location"], data["difficulty"], data["importance"],
                                data["status"],risk_level, data["assigned_agent_id"])
            return new_agent

        except Exception as e:
            raise KeyError(f"Unable to create a new agent, error:{e}")

        finally:
            cursor.close()


    def get_all_missions(self):
        """
            Returns a list of all missions
        """
        cursor = self.conn.cursor(dictionary=True)


        query = """SELECT * FROM missions;"""
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except Exception as e:
            return []
        finally:
            cursor.close()
        if rows:
            return rows
        return []


    def get_mission_by_id(self, id):
        """
            Returns one mission by ID, or None if not exist
        """
        cursor = self.conn.cursor(dictionary=True)

        query = "SELECT * FROM missions WHERE id =%s;"

        try:
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return row
        except Exception as e:
            return None
        finally:
            cursor.close()


    def assign_mission(self, m_id, a_id):
        """
            Assigning a mission to an agent
        """
        cursor = self.conn.cursor()

        query = f"update missions set assigned_agent_id = %s where id = %s;"

        try:
            cursor.execute(query, (a_id, m_id))
            self.conn.commit()
            updated = cursor.rowcount > 0
        except Exception as e:
            return False
        finally:
            cursor.close()

        return updated


    def update_mission_status(self, id, status):
        """
            Used for any mission status change.
        """
        if not self.get_mission_by_id(id):
            return False

        cursor = self.conn.cursor()

        query = f"update missions set status = %s where id = %s;"

        try:
            cursor.execute(query, (status,id))
            self.conn.commit()
            updated = cursor.rowcount > 0
        except Exception as e:
            return False
        finally:
            cursor.close()

        return updated










# get_open_missions_by_agent(id)
# count_all_missions()
# count_by_status(status)
# count_open_missions()
# count_critical_missions()
# get_top_agent()


data = {"title":"2",
        "description":"no",
        "location":"localy",
        "difficulty":5,
        "importance":8,
        "status":"IN_PROGRESS",
        "assigned_agent_id":2}

mission_db = MissionDB()
print(mission_db.update_mission_status(4, "FAILED"))