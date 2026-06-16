from uuid import UUID
from typing import Optional, Any, Dict, List
from supabase import create_client, Client

def get_client(url: str, service_role_key: str) -> Client:
    return create_client(url, service_role_key)

def create_plan(
    supabase: Client,
    session_id: UUID,
    version: int = 1,
    planner_model: Optional[str] = None,
    objective: Optional[str] = None,
    subtopics: Optional[Any] = None,
    selected_agents: Optional[Any] = None,
    execution_plan: Optional[Any] = None,
    estimated_cost: float = 0,
    estimated_tokens: int = 0,
    created_at: Optional[str] = None,
) -> Dict[str, Any]:
    payload = {
        "session_id": str(session_id),
        "version": version,
        "planner_model": planner_model,
        "objective": objective,
        "subtopics": subtopics if subtopics is not None else [],
        "selected_agents": selected_agents if selected_agents is not None else [],
        "execution_plan": execution_plan if execution_plan is not None else {},
        "estimated_cost": estimated_cost,
        "estimated_tokens": estimated_tokens,
        "created_at": created_at,
    }

    try:
        resp = supabase.table("plans").insert(payload).execute()
        return {"data": resp.data[0]} if resp.data else {"data": None}
    except Exception as e:
        return {"error": str(e)}

def get_plan_by_id(supabase: Client, plan_id: UUID) -> Dict[str, Any]:
    try:
        resp = (
            supabase.table("plans")
            .select("*")
            .eq("id", str(plan_id))
            .maybe_single()
            .execute()
        )
        return {"data": resp.data} if resp.data else {"data": None} #type: ignore
    except Exception as e:
        return {"error": str(e)}

def list_plans(
    supabase: Client,
    session_id: Optional[UUID] = None,
    limit: int = 50,
    offset: int = 0,
    order_by: str = "created_at",
    order_desc: bool = True,
) -> Dict[str, Any]:
    try:
        q = supabase.table("plans").select("*")
        if session_id is not None:
            q = q.eq("session_id", str(session_id))

        q = q.order(order_by, desc=order_desc).range(offset, offset + limit - 1)
        resp = q.execute()
        return {"data": resp.data or []}
    except Exception as e:
        return {"error": str(e)}

def update_plan(
    supabase: Client,
    plan_id: UUID,
    version: Optional[int] = None,
    planner_model: Optional[str] = None,
    objective: Optional[str] = None,
    subtopics: Optional[Any] = None,
    selected_agents: Optional[Any] = None,
    execution_plan: Optional[Any] = None,
    estimated_cost: Optional[float] = None,
    estimated_tokens: Optional[int] = None,
    created_at: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}

    if version is not None:
        payload["version"] = version
    if planner_model is not None:
        payload["planner_model"] = planner_model
    if objective is not None:
        payload["objective"] = objective
    if subtopics is not None:
        payload["subtopics"] = subtopics
    if selected_agents is not None:
        payload["selected_agents"] = selected_agents
    if execution_plan is not None:
        payload["execution_plan"] = execution_plan
    if estimated_cost is not None:
        payload["estimated_cost"] = estimated_cost
    if estimated_tokens is not None:
        payload["estimated_tokens"] = estimated_tokens
    if created_at is not None:
        payload["created_at"] = created_at

    if not payload:
        return {"error": "no fields to update"}

    try:
        resp = (
            supabase.table("plans")
            .update(payload)
            .eq("id", str(plan_id))
            .execute()
        )
        return {"updated": True, "result": resp.data}
    except Exception as e:
        return {"error": str(e)}

def delete_plan(supabase: Client, plan_id: UUID) -> Dict[str, Any]:
    try:
        resp = (
            supabase.table("plans")
            .delete()
            .eq("id", str(plan_id))
            .execute()
        )
        return {"deleted": True, "result": resp.data}
    except Exception as e:
        return {"error": str(e)}