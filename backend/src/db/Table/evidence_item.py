from uuid import UUID
from typing import Optional, Any, Dict
import sys
from pathlib import Path

try:
    current_dir = Path(__file__).resolve().parent
except NameError:
    current_dir = Path.cwd()

db_dir = current_dir.parent  # backend/src/db

if str(db_dir) not in sys.path:
    sys.path.insert(0, str(db_dir))

from connection import get_supabase_client
supabase = get_supabase_client()

def create_evidence_item( 
    session_id: UUID,
    agent_run_id: Optional[UUID] = None,
    source_type: Optional[str] = None,
    source_name: Optional[str] = None,
    source_author: Optional[str] = None,
    language: Optional[str] = None,
    title: Optional[str] = None,
    content: Optional[str] = None,
    summary: Optional[str] = None,
    url: Optional[str] = None,
    source_confidence: float = 0,
    relevance_score: float = 0,
    verification_score: float = 0,
    final_confidence: float = 0,
    citation_count: int = 0,
    published_at: Optional[str] = None,
    retrieved_at: Optional[str] = None,
    created_at: Optional[str] = None,
) -> Dict[str, Any]:
    payload = {
        "session_id": str(session_id),
        "agent_run_id": str(agent_run_id) if agent_run_id is not None else None,
        "source_type": source_type,
        "source_name": source_name,
        "source_author": source_author,
        "language": language,
        "title": title,
        "content": content,
        "summary": summary,
        "url": url,
        "source_confidence": source_confidence,
        "relevance_score": relevance_score,
        "verification_score": verification_score,
        "final_confidence": final_confidence,
        "citation_count": citation_count,
        "published_at": published_at,
        "retrieved_at": retrieved_at,
        "created_at": created_at,
    }

    try:
        resp = supabase.table("evidence_items").insert(payload).execute()
        return {"data": resp.data[0]} if resp.data else {"data": None}
    except Exception as e:
        return {"error": str(e)}

def get_evidence_item_by_id(evidence_id: UUID) -> Dict[str, Any]:
    try:
        resp = (
            supabase.table("evidence_items")
            .select("*")
            .eq("id", str(evidence_id))
            .maybe_single()
            .execute()
        )
        return {"data": resp.data} if resp.data else {"data": None} #type: ignore
    except Exception as e:
        return {"error": str(e)}

def list_evidence_items(
    session_id: Optional[UUID] = None,
    agent_run_id: Optional[UUID] = None,
    limit: int = 50,
    offset: int = 0,
    order_by: str = "created_at",
    order_desc: bool = True,
) -> Dict[str, Any]:
    try:
        q = supabase.table("evidence_items").select("*")

        if session_id is not None:
            q = q.eq("session_id", str(session_id))
        if agent_run_id is not None:
            q = q.eq("agent_run_id", str(agent_run_id))

        q = q.order(order_by, desc=order_desc).range(offset, offset + limit - 1)
        resp = q.execute()
        return {"data": resp.data or []}
    except Exception as e:
        return {"error": str(e)}

def update_evidence_item(
    evidence_id: UUID,
    agent_run_id: Optional[UUID] = None,
    source_type: Optional[str] = None,
    source_name: Optional[str] = None,
    source_author: Optional[str] = None,
    language: Optional[str] = None,
    title: Optional[str] = None,
    content: Optional[str] = None,
    summary: Optional[str] = None,
    url: Optional[str] = None,
    source_confidence: Optional[float] = None,
    relevance_score: Optional[float] = None,
    verification_score: Optional[float] = None,
    final_confidence: Optional[float] = None,
    citation_count: Optional[int] = None,
    published_at: Optional[str] = None,
    retrieved_at: Optional[str] = None,
    created_at: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}

    if agent_run_id is not None:
        payload["agent_run_id"] = str(agent_run_id)
    if source_type is not None:
        payload["source_type"] = source_type
    if source_name is not None:
        payload["source_name"] = source_name
    if source_author is not None:
        payload["source_author"] = source_author
    if language is not None:
        payload["language"] = language
    if title is not None:
        payload["title"] = title
    if content is not None:
        payload["content"] = content
    if summary is not None:
        payload["summary"] = summary
    if url is not None:
        payload["url"] = url
    if source_confidence is not None:
        payload["source_confidence"] = source_confidence
    if relevance_score is not None:
        payload["relevance_score"] = relevance_score
    if verification_score is not None:
        payload["verification_score"] = verification_score
    if final_confidence is not None:
        payload["final_confidence"] = final_confidence
    if citation_count is not None:
        payload["citation_count"] = citation_count
    if published_at is not None:
        payload["published_at"] = published_at
    if retrieved_at is not None:
        payload["retrieved_at"] = retrieved_at
    if created_at is not None:
        payload["created_at"] = created_at

    if not payload:
        return {"error": "no fields to update"}

    try:
        resp = (
            supabase.table("evidence_items")
            .update(payload)
            .eq("id", str(evidence_id))
            .execute()
        )
        return {"updated": True, "result": resp.data}
    except Exception as e:
        return {"error": str(e)}

def delete_evidence_item(evidence_id: UUID) -> Dict[str, Any]:
    try:
        resp = (
            supabase.table("evidence_items")
            .delete()
            .eq("id", str(evidence_id))
            .execute()
        )
        return {"deleted": True, "result": resp.data}
    except Exception as e:
        return {"error": str(e)}