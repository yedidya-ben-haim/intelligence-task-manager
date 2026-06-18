from db_connection import ConnectionDB



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



    def get_agent_by_id(self, id):
        """
            Returns one agent by ID, or None if not exist
        """
        cursor = self.conn.cursor(dictionary=True)

        query = "SELECT * FROM agents WHERE id =%s;"

        try:
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return row
        except Exception as e:
            return None
        finally:
            cursor.close()


    # todo: Check ID change
    def update_agent(self ,id, data: dict):
        """
            UPDATE agent for the entire row (cannot change id)
            Return TRUE/FALSE
        """
        if not self.get_agent_by_id(id):
            print("The agent was not found.")
            return False

        cursor = self.conn.cursor(dictionary=True)


        in_part = [f"{key}=%s" for key in data]
        in_str = ", ".join(in_part)
        value = list(data.values())+ [id]

        query = f"update agents set {in_str} where id = %s;"

        try:
            cursor.execute(query, value)
            self.conn.commit()
            updated = cursor.rowcount > 0
        except Exception as e:
            return False
        finally:
            cursor.close()

        return updated


data = {"title":"2",
        "description":"no",
        "location":"localy",
        "difficulty":5,
        "importance":8,
        "status":"IN_PROGRESS",
        "assigned_agent_id":2}

mission_db = MissionDB()
print(mission_db.get_all_missions())