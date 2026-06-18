from fastapi import APIRouter,HTTPException
from logs.log_step import app_logger
from database.agent_db import AgentDB
from database.mission_db import MissionDB
from pydantic import BaseModel



router = APIRouter()
agent_db = AgentDB()
mission_db = MissionDB()


class CreateMission(BaseModel):
    pass



class UpdateMission(BaseModel):
    pass


@router.post("/missions",status_code=201)
def create_mission(data):
    pass


@router.get("/missions")
def get_all_missions():
    all_mission = mission_db.get_all_missions()

    return {"message":"all mission" , "data":all_mission}

@router.get("/missions/{id}")
def get_mission_by_id(id: int):
    mission = mission_db.get_mission_by_id(id)

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return {"message":f"mission{id}", "data":mission}


@router.put("/missions/{id}/assign/{agent_id}")
def assign_mission(id: int, agent_id: int):
    mission = mission_db.get_mission_by_id(id)
    agent = agent_db.get_agent_by_id(agent_id)

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if mission.get("status") != 'NEW':
        raise HTTPException(status_code=400, detail="Mission not available")
    if not agent.get("is_active"):
        raise HTTPException(status_code=400, detail="Agent is not active")
    if mission_db.get_open_missions_by_agent(agent_db) > 3:
        raise HTTPException(status_code=400, detail="Agent has reached maximum missions")
    if mission.get("risk_level") == "CRITICAL":
        if agent.get("agent_rank") != "Commander":
            raise HTTPException(status_code=400, detail="Only Commander can handle critical missions")

    mission_db.assign_mission(id, agent_id)
    return {"message":"ASSIGNED", "data":""}

@router.put("/missions/{id}/start")
def start_mission(id: int):
    mission = mission_db.get_mission_by_id(id)

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if mission.get("status") != "ASSIGNED":
        raise HTTPException(status_code=400, detail="Mission not ASSIGNED")

    mission_db.update_mission_status(id, "IN_PROGRESS")
    return {"message":"IN_PROGRESS", "data":""}



@router.put("/missions/{id}/complete")
def complete_mission(id: int):
    mission = mission_db.get_mission_by_id(id)

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if mission.get("status") != "IN_PROGRESS":
        raise HTTPException(status_code=400, detail="Mission not IN_PROGRESS")

    mission_db.update_mission_status(id, "COMPLETED")
    assigned_agent_id = mission.get("assigned_agent_id")
    agent_db.increment_completed(assigned_agent_id)
    return {"message":"COMPLETED", "data":""}


@router.put("/missions/{id}/fail")
def fail_mission(id: int):
    mission = mission_db.get_mission_by_id(id)

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if mission.get("status") != "IN_PROGRESS":
        raise HTTPException(status_code=400, detail="Mission not IN_PROGRESS")

    mission_db.update_mission_status(id, "FAILED")
    assigned_agent_id = mission.get("assigned_agent_id")
    agent_db.increment_failed(assigned_agent_id)
    return {"message":"FAILED", "data":""}


@router.put("/missions/{id}/cancel")
def cancel_mission(id: int):
    mission = mission_db.get_mission_by_id(id)

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if mission.get("status") != ("NEW" or "ASSIGNED"):
        raise HTTPException(status_code=400, detail="Mission not NEW or ASSIGNED")

    mission_db.update_mission_status(id, "CANCELLED")
    return {"message":"CANCELLED", "data":""}