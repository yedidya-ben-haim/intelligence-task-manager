from fastapi import APIRouter,HTTPException
from logs.log_step import app_logger
from database.agent_db import AgentDB

router = APIRouter()
agent_db = AgentDB()


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
    return all_agents


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
    return all_agents




