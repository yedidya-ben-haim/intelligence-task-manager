from fastapi import APIRouter,HTTPException
from logs.log_step import app_logger
from database.agent_db import AgentDB
from pydantic import BaseModel



router = APIRouter()
agent_db = AgentDB()


class CreateAgent(BaseModel):
    name: str
    agent_rank : str
    specialty: str







@router.get("/agents")
def get_all_agents():
    app_logger.info("get /agents called")
    try:
        app_logger.info("operation agent_db.get_all_agents()")
        all_agents = agent_db.get_all_agents()
    except Exception as e:
        app_logger.error("all agents not found")
        raise HTTPException(status_code=404, detail="get /agents called failed")

    app_logger.info("get /agents Successfully completed")
    return {"message":"all agent" , "data":all_agents}


@router.get("/agents/{id}")
def get_agent_by_id(id: int):
    app_logger.info("get /agents/{id} called")
    try:
        app_logger.info("operation agent_db.get_agent_by_id(id)")
        agent = agent_db.get_agent_by_id(id)
    except Exception as e:
        app_logger.error("agent by id not found")
        raise HTTPException(status_code=404, detail=f"{e}")
    if not agent:
        raise HTTPException(status_code=404, detail="agent by id not found")

    app_logger.info("get /agents/{id} Successfully completed")
    return {"message":"agent", "data":agent}


@router.get("/agents/{id}/performance")
def get_agent_performance(id: int):
    app_logger.info("get /agents/{id}/performance called")
    try:
        app_logger.info("operation agent_db.get_agent_performance(id)")
        agent = agent_db.get_agent_performance(id)
    except Exception as e:
        app_logger.error("agent by id not found")
        raise HTTPException(status_code=404, detail=f"{e}")
    if not agent:
        raise HTTPException(status_code=404, detail="agent not exist")

    app_logger.info("get /agents/{id}/performance Successfully completed")
    return {"message":"agent", "data":agent}


@router.post("/agents",status_code=201)
def create_agent(data: CreateAgent):
    data = data.model_dump()
    vailed_agent_rank = ["Junior", "Senior", "Commander"]

    print("hi")
    if data.get("agent_rank") not in vailed_agent_rank:
        HTTPException(status_code=400, detail="Invalid rank")
    if not data:
        HTTPException(status_code=422, detail="no data")

    agent = agent_db.create_agent(data)
    return agent.__dict__


@router.put("/agents/{id}")
def update_agent(id: int, data: dict[]):
    agent = agent_db.get_agent_by_id(id)
    if not agent:
        raise HTTPException(status_code=404, detail="agent by id not found")
    if not data:
        HTTPException(status_code=422, detail="no data")

    agent_db.update_agent(id, data)
    return {"message": "Updated", "data": agent}



@router.put("/agents/{id}/deactivate")
def deactivate_agent(id: int):
    agent = agent_db.get_agent_by_id(id)
    if not agent:
        raise HTTPException(status_code=404, detail="agent by id not found")

    agent_db.deactivate_agent(id)
    return {"message":"is_active=False", "data":""}

