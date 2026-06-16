import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

current_dir = Path(__file__).resolve().parent
db_dir = current_dir.parent  # backend/src/db

if str(db_dir) not in sys.path:
    sys.path.insert(0, str(db_dir)) 
    
from connection import get_supabase_client

TABLE = "reports"

supabase = get_supabase_client()

# ─────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────

def create_report(
    session_id: str,
    title: str,
    report_type: Optional[str] = None,
    summary: Optional[str] = None,
    report_status: str = "draft",
    overall_score: float = 0.0,
    confidence_score: float = 0.0,
    citation_count: int = 0,
    evidence_count: int = 0,
    claim_count: int = 0,
    word_count: int = 0,
    reading_time_minutes: int = 0,
    generation_tokens: int = 0,
    generation_cost: float = 0.0,
    markdown_content: Optional[str] = None,
    structured_content: Optional[dict] = None,
    metadata: Optional[dict] = None,
    version: int = 1,
) -> dict:
    """Insert a new report row."""
    payload = {
        "session_id": session_id,
        "title": title,
        "version": version,
        "report_type": report_type,
        "summary": summary,
        "report_status": report_status,
        "overall_score": overall_score,
        "confidence_score": confidence_score,
        "citation_count": citation_count,
        "evidence_count": evidence_count,
        "claim_count": claim_count,
        "word_count": word_count,
        "reading_time_minutes": reading_time_minutes,
        "generation_tokens": generation_tokens,
        "generation_cost": str(generation_cost),  # numeric → string for safety
        "markdown_content": markdown_content,
        "structured_content": structured_content or {},
        "metadata": metadata or {},
    }
    response = supabase.table(TABLE).insert(payload).execute()
    return response.data[0]


# ─────────────────────────────────────────
# READ
# ─────────────────────────────────────────

def get_report_by_id(report_id: str) -> Optional[dict[str, Any]]:
    """Fetch a single report by its UUID."""
    response = (
        supabase.table(TABLE)
        .select("*")
        .eq("id", report_id)
        .single()
        .execute()
    )
    return response.data


def get_reports_by_session(
    session_id: str,
    status: Optional[str] = None,
    report_type: Optional[str] = None,
    order_by: str = "created_at",
    ascending: bool = False,
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """Fetch all reports for a session with optional filters."""
    query = (
        supabase.table(TABLE)
        .select("*")
        .eq("session_id", session_id)
    )
    if status:
        query = query.eq("report_status", status)
    if report_type:
        query = query.eq("report_type", report_type)

    query = query.order(order_by, desc=not ascending)
    query = query.range(offset, offset + limit - 1)

    response = query.execute()
    return response.data


def list_reports(
    status: Optional[str] = None,
    report_type: Optional[str] = None,
    min_score: Optional[float] = None,
    order_by: str = "created_at",
    ascending: bool = False,
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """List reports across all sessions with optional filters."""
    query = supabase.table(TABLE).select("*")

    if status:
        query = query.eq("report_status", status)
    if report_type:
        query = query.eq("report_type", report_type)
    if min_score is not None:
        query = query.gte("overall_score", min_score)

    query = query.order(order_by, desc=not ascending)
    query = query.range(offset, offset + limit - 1)

    response = query.execute()
    return response.data


# ─────────────────────────────────────────
# UPDATE
# ─────────────────────────────────────────

def update_report(report_id: str, **fields) -> dict:
    """
    Partial update — pass only the fields you want to change.

    Example:
        update_report(id, report_status="published", overall_score=8.5)
    """
    if not fields:
        raise ValueError("No fields provided for update.")

    # Coerce generation_cost to string if present
    if "generation_cost" in fields:
        fields["generation_cost"] = str(fields["generation_cost"])

    fields["updated_at"] = datetime.now(timezone.utc).isoformat()

    response = (
        supabase.table(TABLE)
        .update(fields)
        .eq("id", report_id)
        .execute()
    )
    return response.data[0]


def publish_report(report_id: str) -> dict:
    """Convenience: mark a report as published."""
    return update_report(report_id, report_status="published")


def bump_version(report_id: str) -> dict:
    """Increment the version number by 1."""
    current = get_report_by_id(report_id)
    if not current:
        raise ValueError(f"Report {report_id} not found.")
    return update_report(report_id, version=current["version"] + 1)


def update_scores(
    report_id: str,
    overall_score: float,
    confidence_score: float,
) -> dict:
    """Convenience: update both score fields at once."""
    return update_report(
        report_id,
        overall_score=overall_score,
        confidence_score=confidence_score,
    )


# ─────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────

def delete_report(report_id: str) -> bool:
    """Hard-delete a report by ID. Returns True if a row was deleted."""
    response = (
        supabase.table(TABLE)
        .delete()
        .eq("id", report_id)
        .execute()
    )
    return len(response.data) > 0


def delete_reports_by_session(session_id: str) -> int:
    """
    Delete all reports belonging to a session.
    (Cascade on the FK handles this automatically, but this is explicit.)
    Returns count of deleted rows.
    """
    response = (
        supabase.table(TABLE)
        .delete()
        .eq("session_id", session_id)
        .execute()
    )
    return len(response.data)


# ─────────────────────────────────────────
# UPSERT
# ─────────────────────────────────────────

def upsert_report(report_data: dict) -> dict:
    """
    Insert or update a report.
    Requires 'id' to be present in report_data for update path.
    """
    if "generation_cost" in report_data:
        report_data["generation_cost"] = str(report_data["generation_cost"])
    report_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    response = (
        supabase.table(TABLE)
        .upsert(report_data, on_conflict="id")
        .execute()
    )
    return response.data[0]