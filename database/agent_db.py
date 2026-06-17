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

        cursor.execute(query)
        rows = cursor.fetchall()

        cursor.close()

        return rows







        try:
            cursor.execute(query, value)
            self.conn.commit()

            new_agent = Agent(data["name"], data["specialty"], data["agent_rank"])
            return new_agent

        except Exception as e:
            raise KeyError(f"Unable to create a new agent, error:{e}")

        finally:
            cursor.close()

    def get_agent_by_id(self, id):
        pass


    def update_agent(self ,id, data):
        pass


    def deactivate_agent(self,id):
        pass


    def increment_completed(self, id):
        pass


    def increment_failed(self, id):
        pass


    def get_agent_performance(self, id):
        pass


    def count_active_agents(self):
        pass







data = {"name":"avi", "specialty":"plenner", "agent_rank":"Junior"}


new_agent_db = AgentDB()
print(new_agent_db.get_all_agents())

