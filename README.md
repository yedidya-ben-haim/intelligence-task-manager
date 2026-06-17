# intelligence-task-manager

---


## Project Description

The project is an agent and mission management system that allows you to manage a database of agents,
including information about them, as well as manage a database of missions, including detailed information about the mission, including an interface to add and remove missions and agents.


---



## Folder Structure

```
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Database Information

**Database Name:** Intelligence_db


---

## Database Tables


### Table: `agents`

| Column Name        | Data Type      | Constraints    | Description                              |
|--------------------|----------------|----------------|------------------------------------------|
| id                 | PRIMARY KEY    | AUTO_INCREMENT | Unique identifier                        |
| name               | VARCHAR(50)    | NOT NULL       | Agent name                               |
| specialty          | VARCHAR(50)    | NOT NULL       | Field of specialization                  |
| is_active          | BOOLEAN        | DEFAULT TRUE   | Is the agent active                      |
| completed_missions | INT            | DEFAULT 0      | Completed missions                       |
| failed_missions    | INT            | DEFAULT 0      | Failed missions                          |
| agent_rank         | ENUM / VARCHAR | ENUM / VARCHAR | Agent Rank (Junior / Senior / Commander) |



### Table: `missions`

| Column Name       | Data Type    | Constraints              | Description                                                               |
|-------------------|--------------|--------------------------|---------------------------------------------------------------------------|
| id                | PRIMARY KEY  | AUTO_INCREMENT           | Unique identifier                                                         |
| title             | VARCHAR(50)  | NOT NULL                 | Mission title                                                             |
| description       | TEXT         | NOT NULL                 | Detailed description of mission                                           |
| location          | VARCHAR(100) | NOT NULL                 | Mission location                                                          |
| difficulty        | INT          | 1-10                     | Difficulty level                                                          |
| importance        | INT          | 1-10                     | Level of importance                                                       |
| status            | VARCHAR(50)  | DEFAULT NEW              | Mission status (NEW, ASSIGNED, IN_PROGRESS, COMPLETED, FAILED, CANCELLED) |
| risk_level        | VARCHAR(50)  | AUTOMATICALLY CALCULATED |                                                                           |
| assigned_agent_id | INT          | DEFAULT NULL             | Agent association                                                         |





___

## Explanation of classes

### db_connection

Responsible for connecting to the MySQL container, creating the database, and creating the tables.



| Method             | Description                                  |
|--------------------|----------------------------------------------|
| get_connection()   | Returns an active connection to MySQL        |
| create_database()  | Creates Intelligence_db if it does not exist |
| create_tables()    | Creates both tables if they do not exist.    |




### AgentDB

Responsible for managing the agent table including creating agent objects.


| Method                    | Return            | Description                                                                 |
|---------------------------|-------------------|-----------------------------------------------------------------------------|
| create_agent(data)        | agent object      | Creates a new agent and returns the agent object.                           |
| get_all_agents()          | LIST[Dictionary]  | Returns a list of all agents                                                |
| get_agent_by_id(id)       | Dictionary\None   | Returns one agent by ID, or None                                            |
| update_agent(id, data)    | TRUE/FALSE        | UPDATE for the entire row (cannot change id)                                |
| deactivate_agent(id)      | TRUE/FALSE        | Sets agent is_active=False.                                                 |
| increment_completed(id)   | TRUE/FALSE        | Updates the number of missions completed.                                   |
| increment_failed(id)      | TRUE/FALSE        | Updates the number of failed missions                                       |
| get_agent_performance(id) | Dictionary        | Returns a dictionary with the keys (completed, failed, total, success_rate) |
| count_active_agents()     | INT               | Returns the number of active agents                                         |



### MissionDB

Responsible for managing the mission table including creating mission objects.


| Method                            | Return           | Description                                          |
|-----------------------------------|------------------|------------------------------------------------------|
| create_mission(data)              | mission object   | Creates a new mission and returns the mission object |
| get_all_missions()                | LIST[Dictionary] | Returns all missions                                 |
| get_mission_by_id(id)             | Dictionary\None  | Returns one mission by ID, or None                   |
| assign_mission(m_id, a_id)        | TRUE/FALSE       | Assigning a mission to an agent                      |
| update_mission_status(id, status) | TRUE/FALSE       | Used for any status change                           |
| get_open_missions_by_agent(id)    | LIST[Dictionary] | Returns agent ASSIGNED/IN_PROGRESS missions          |
| count_all_missions()              | INT              | Total missions                                       |
| count_by_status(status)           | INT              | Counts missions by a specific status                 |
| count_open_missions()             | INT              | Open mission counter                                 |
| count_critical_missions()         | INT              | CRITICAL mission counter                             |
| get_top_agent()                   | Dictionary       | The agent with the highest completed_missions        |



---



## System Rules

1. rank must be Junior / Senior / Commander — any other value throws an error
2. Difficulty and importance must be between 1 and 10 — otherwise an error. 
3. risk_level is calculated automatically when creating a mission — the user does not send it. 
4. An agent with is_active=False cannot accept missions. 
5. An agent cannot have more than 3 open missions (ASSIGNED / IN_PROGRESS) at the same time. 
6. If risk_level=CRITICAL — only an agent with the Commander rank can accept the mission. 
7. Only a mission with the NEW status can be assigned. After assignment: status=ASSIGNED.
8. Only a mission with the ASSIGNED status can be started. After: status=IN_PROGRESS.
9. Only a mission with the IN_PROGRESS status can be terminated and changed to failed or completed. 
10. Only a mission with the NEW or ASSIGNED status can be canceled — otherwise an error.

---


## Installation


1. Clone the repository:

```bash
https://github.com/yedidya-ben-haim/intelligence-task-manager.git
```

2. Install venv environment

```bash
python -m venv .venv         
```

3. Activate the virtual environment

```bash
.\.venv\Scripts\activate  
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up the docker and database:

```bash
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
```

---

docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
