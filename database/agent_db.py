from db_connection import ConnectionDB



# todo: Improvement
class Agent:
    def __init__(self, name, specialty, agent_rank):
        self.name = name
        self.specialty = specialty
        self.agent_rank = agent_rank




class AgentDB:
    """
        Responsible for managing the agent table including creating agent objects.
    """

    def __init__(self):
        self.conn = ConnectionDB().get_connection()


    def create_agent(self, data: dict):
        """
            Creates a new agent and returns the agent object.
        """
        cursor = self.conn.cursor()

        value = (data["name"], data["specialty"], data["agent_rank"])

        query = """insert into agents (name, specialty, agent_rank)
                                values (%s, %s,%s);
                """

        try:
            cursor.execute(query, value)
            self.conn.commit()

            new_agent = Agent(data["name"], data["specialty"], data["agent_rank"])
            return new_agent

        except Exception as e:
            raise KeyError(f"Unable to create a new agent, error:{e}")

        finally:
            cursor.close()


    def get_all_agents(self):
        """
            Returns a list of all agents
        """
        cursor = self.conn.cursor(dictionary=True)


        query = """SELECT * FROM agents;"""
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


    def deactivate_agent(self,id):
        """
            Updating agent is_active=False.
        """
        if not self.get_agent_by_id(id):
            return False

        cursor = self.conn.cursor()

        query = f"update agents set is_active = FALSE where id = %s;"

        try:
            cursor.execute(query, (id,))
            self.conn.commit()
            updated = cursor.rowcount > 0
        except Exception as e:
            return False
        finally:
            cursor.close()

        return updated


    def increment_completed(self, id):
        """
            Updates the number of missions completed.
        """
        if not self.get_agent_by_id(id):
            return False

        cursor = self.conn.cursor()

        query = f"update agents set completed_missions = completed_missions + 1 where id = %s;"

        try:
            cursor.execute(query, (id,))
            self.conn.commit()
            updated = cursor.rowcount > 0
        except Exception as e:
            return False
        finally:
            cursor.close()

        return updated


    def increment_failed(self, id):
        """
           Updates the number of failed missions.
       """
        if not self.get_agent_by_id(id):
            return False

        cursor = self.conn.cursor()

        query = f"update agents set failed_missions = failed_missions + 1 where id = %s;"

        try:
            cursor.execute(query, (id,))
            self.conn.commit()
            updated = cursor.rowcount > 0
        except Exception as e:
            return False
        finally:
            cursor.close()

        return updated


    def get_agent_performance(self, id):
        """
            Returns a dictionary with the keys (completed, failed, total, success_rate)
        """
        agent = self.get_agent_by_id(id)

        if not agent:
            return False

        completed = agent["completed_missions"]
        failed = agent["failed_missions"]
        total = completed + failed

        if total > 0:
            success_rate = (completed/total) * 100
        else:
            success_rate = 0.0

        performance = {"completed":completed,
                       "failed":failed,
                       "total": total,
                       "success_rate":success_rate}

        return performance


    def count_active_agents(self):
        """
            Returns the number of active agents
        """

        cursor = self.conn.cursor(dictionary=True)

        query = "SELECT COUNT(*) as count FROM agents WHERE is_active = 1;"
        try:
            cursor.execute(query)
            row = cursor.fetchone()
            return row["count"]
        except Exception as e:
            return 0
        finally:
            cursor.close()





# todo: delete
#
# data = {"name":"avi", "specialty":"plenner", "agent_rank":"Junior"}
#
#
# new_agent_db = AgentDB()
# print(new_agent_db.count_active_agents())


