import asyncio
import os
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
db_dir = current_dir.parent  # backend/src/db

if str(db_dir) not in sys.path:
    sys.path.insert(0, str(db_dir)) 
    
from connection import get_supabase_client

# ─── CREATE ───────────────────────────────────────────────────────────────────

async def insert_research_session(
    user_id, title, topic=None, research_type=None, report_goal=None,
    target_audience=None, requested_depth=None, priority=None,
    execution_strategy=None, selected_agents=None,
):
    supabase = get_supabase_client()
    payload = {
        "user_id": user_id,
        "title": title,
        "topic": topic,
        "research_type": research_type,
        "report_goal": report_goal,
        "target_audience": target_audience,
        "requested_depth": requested_depth,
        "priority": priority,
        "execution_strategy": execution_strategy,
        "selected_agents": selected_agents or [],
    }
    try:
        res = supabase.table("research_sessions").insert(payload).execute()
        if getattr(res, "error", None):
            print(f"Failed to insert research session: {title}")
            return False
        if isinstance(res.data, list) and res.data and isinstance(res.data[0], dict):
            session_id = res.data[0].get("id")
            if session_id is not None:
                print(f"Research session created. ID: {session_id}")
                return session_id
        print(f"Failed to create research session: {title}")
        return False
    except Exception as e:
        print(f"Error creating research session '{title}': {e}")
        return False


# ─── READ (single) ────────────────────────────────────────────────────────────

async def get_research_session(session_id):
    supabase = get_supabase_client()
    try:
        res = (
            supabase.table("research_sessions")
            .select("*")
            .eq("id", session_id)
            .single()
            .execute()
        )
        if getattr(res, "error", None):
            print(f"Failed to fetch research session: {session_id}")
            return None
        return res.data
    except Exception as e:
        print(f"Error fetching research session '{session_id}': {e}")
        return None


# ─── READ (list by user) ──────────────────────────────────────────────────────

async def get_research_sessions_by_user(user_id):
    supabase = get_supabase_client()
    try:
        res = (
            supabase.table("research_sessions")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        if getattr(res, "error", None):
            print(f"Failed to fetch sessions for user: {user_id}")
            return []
        return res.data or []
    except Exception as e:
        print(f"Error fetching sessions for user '{user_id}': {e}")
        return []


# ─── UPDATE ───────────────────────────────────────────────────────────────────

async def update_research_session(session_id, **fields):
    """
    Pass only the fields you want to update, e.g.:
        await update_research_session(session_id, title="New Title", priority="high")
    """
    if not fields:
        print("No fields provided for update.")
        return False

    supabase = get_supabase_client()
    try:
        res = (
            supabase.table("research_sessions")
            .update(fields)
            .eq("id", session_id)
            .execute()
        )
        if getattr(res, "error", None):
            print(f"Failed to update research session: {session_id}")
            return False
        print(f"Research session updated. ID: {session_id}")
        return True
    except Exception as e:
        print(f"Error updating research session '{session_id}': {e}")
        return False


# ─── DELETE ───────────────────────────────────────────────────────────────────

async def delete_research_session(session_id):
    supabase = get_supabase_client()
    try:
        res = (
            supabase.table("research_sessions")
            .delete()
            .eq("id", session_id)
            .execute()
        )
        if getattr(res, "error", None):
            print(f"Failed to delete research session: {session_id}")
            return False
        print(f"Research session deleted. ID: {session_id}")
        return True
    except Exception as e:
        print(f"Error deleting research session '{session_id}': {e}")
        return False
    

async def main():
    create = await insert_research_session(user_id="c72f18f7-9089-4ba4-8253-39abf8c54f98" , title="Test Session", topic="AI Research", research_type="exploratory")
    
    print(create)
    
if __name__ == "__main__":
    asyncio.run(main())