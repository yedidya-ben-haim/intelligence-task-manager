from fastapi import APIRouter,HTTPException
from logs.log_step import app_logger
from database.agent_db import AgentDB
from database.mission_db import MissionDB




router = APIRouter()
agent_db = AgentDB()
mission_db = MissionDB()


@router.get("/reports/summary")
def summary_reports():

    active_agents_count = agent_db.count_active_agents()
    total_missions = mission_db.count_all_missions()
    open_missions = mission_db.count_open_missions()
    completed_missions = mission_db.count_by_status("COMPLETED")
    failed_missions = mission_db.count_by_status("FAILED")
    critical_missions = mission_db.count_critical_missions()

    return {
            "active_agents_count":active_agents_count,
            "total_missions":total_missions,
            "open_missions": open_missions,
            "completed_missions":completed_missions,
            "failed_missions":failed_missions,
            "critical_missions":critical_missions
            }



@router.get("/reports/missions-by-status")
def missions_by_status_reports():
    open = mission_db.count_open_missions()
    in_progress = mission_db.count_by_status("IN_PROGRESS")
    completed = mission_db.count_by_status("COMPLETED")
    failed = mission_db.count_by_status("FAILED")
    critical = mission_db.count_critical_missions()

    return {
            "open": open,
            "in_progress": in_progress,
            "completed": completed,
            "failed": failed,
            "critical": critical
        }


@router.get("/reports/top-agent")
def get_top_agent():
    return mission_db.get_top_agent()
