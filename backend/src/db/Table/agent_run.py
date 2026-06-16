from uuid import UUID
from typing import Optional, Any, Dict
import asyncio 
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
db_dir = current_dir.parent  # backend/src/db

if str(db_dir) not in sys.path:
    sys.path.insert(0, str(db_dir)) 
    
from connection import get_supabase_client
 
supabase = get_supabase_client()

def create_agent_run( 
    session_id,
    agent_name: str,
    agent_type: Optional[str] = None,
    model_used: Optional[str] = None,
    status: str = "pending",
    retry_count: int = 0,
    token_usage: int = 0,
    execution_cost: float = 0,
    execution_time: float = 0,
    evidence_generated: int = 0,
    error_message: Optional[str] = None,
    started_at: Optional[str] = None,
    completed_at: Optional[str] = None,
) :
    payload = {
        "session_id": str(session_id),
        "agent_name": agent_name,
        "agent_type": agent_type,
        "model_used": model_used,
        "status": status,
        "retry_count": retry_count,
        "token_usage": token_usage,
        "execution_cost": execution_cost,
        "execution_time": execution_time,
        "evidence_generated": evidence_generated,
        "error_message": error_message,
        "started_at": started_at,
        "completed_at": completed_at,
    }
    try:
        resp = supabase.table("agent_runs").insert(payload).execute()
        return resp
    except Exception as e:
        return {"error": str(e)}

def get_agent_run_by_id(run_id) :
    try:
        resp = (
            supabase.table("agent_runs")
            .select("*")
            .eq("id", str(run_id))
            .maybe_single()
            .execute()
        )
        return resp
    except Exception as e:
        return {"error": str(e)}

def list_agent_runs(
    session_id: None,
    limit: int = 50,
    offset: int = 0,
    order_by: str = "started_at",
    order_desc: bool = True,
) -> Any:
    try:
        q = supabase.table("agent_runs").select("*")
        if session_id is not None:
            q = q.eq("session_id", str(session_id))
        q = q.order(order_by, desc=order_desc).range(offset, offset + limit - 1)
        resp = q.execute()
        return resp.data
    except Exception as e:
        return {"error": str(e)}

def update_agent_run(
    run_id,
    status: Optional[str] = None,
    retry_count: Optional[int] = None,
    token_usage: Optional[int] = None,
    execution_cost: Optional[float] = None,
    execution_time: Optional[float] = None,
    evidence_generated: Optional[int] = None,
    error_message: Optional[str] = None,
    started_at: Optional[str] = None,
    completed_at: Optional[str] = None,
    agent_name: Optional[str] = None,
    agent_type: Optional[str] = None,
    model_used: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    
    payload = {}
    
    if status is not None:
        payload["status"] = status
    if retry_count is not None:
        payload["retry_count"] = retry_count
    if token_usage is not None:
        payload["token_usage"] = token_usage
    if execution_cost is not None:
        payload["execution_cost"] = execution_cost
    if execution_time is not None:
        payload["execution_time"] = execution_time
    if evidence_generated is not None:
        payload["evidence_generated"] = evidence_generated
    if error_message is not None:
        payload["error_message"] = error_message
    if started_at is not None:
        payload["started_at"] = started_at
    if completed_at is not None:
        payload["completed_at"] = completed_at
    if agent_name is not None:
        payload["agent_name"] = agent_name
    if agent_type is not None:
        payload["agent_type"] = agent_type
    if model_used is not None:
        payload["model_used"] = model_used

    if not payload:
        return {"error": "no fields to update"}

    try:
        resp = (
            supabase.table("agent_runs")
            .update(payload)
            .eq("id", str(run_id))
            .execute()
        )
        return {"updated": True, "result": resp.data}
    except Exception as e:
        return {"error": str(e)}

def delete_agent_run(run_id) -> bool:
    
    try:
        resp = supabase.table("agent_runs").delete().eq("id", str(run_id)).execute()
        return True if resp.data is not None else True
    except Exception as e:
        return False
    


# async def main():

    # run = create_agent_run(
    #     session_id="e2b724f7-1bfd-4394-9594-847a6f7c9b9a",
    #     agent_name="researcher",
    #     agent_type="worker",
    #     model_used="gpt-4.1",
    # )

    # run_id = run["id"] if isinstance(run, dict) and "id" in run else None

#     run_id = "0f63c9f9-e2a3-4fa3-9474-35d3879e59bc"
#     if run_id:
#         print(f"Testing with run_id: {run_id}")
#         created = get_agent_run_by_id(run_id=run_id)
#         print("Created:", created)
#         print("Updating run...")
#         updated = update_agent_run(run_id=run_id, status="completed", completed_at="2026-06-16T00:00:00Z")
#         print("Updated:", updated)
#         ok = delete_agent_run(run_id=run_id)
#         print("Deleted:", ok)        

# if __name__ == "__main__":
#     asyncio.run(main())