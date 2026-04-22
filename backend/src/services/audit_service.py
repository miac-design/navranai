"""
Phase 19: Audit Trail Service.

Logs every action (create, edit, approve, reject, regenerate) with timestamps
and user IDs for full accountability.
"""
import logging
import uuid
import json
from datetime import datetime
from typing import Optional
from src.models import AuditEntry, get_session

logger = logging.getLogger("redm.audit")


class AuditService:
    """Immutable audit trail for all campaign actions."""

    def log(
        self,
        campaign_id: str,
        action: str,
        user_id: str = "system",
        post_id: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        """Log an audit entry."""
        try:
            with get_session() as session:
                entry = AuditEntry(
                    id=uuid.uuid4().hex[:12],
                    campaign_id=campaign_id,
                    post_id=post_id,
                    action=action,
                    user_id=user_id,
                    details=json.dumps(details or {}),
                    timestamp=datetime.utcnow(),
                )
                session.add(entry)
                session.commit()
            logger.info("AUDIT: [%s] %s on campaign %s", user_id, action, campaign_id)
        except Exception as e:
            logger.error("Audit log failed: %s", e)

    def get_campaign_history(self, campaign_id: str) -> list[dict]:
        """Get full audit history for a campaign."""
        try:
            with get_session() as session:
                from sqlmodel import select
                stmt = (
                    select(AuditEntry)
                    .where(AuditEntry.campaign_id == campaign_id)
                    .order_by(AuditEntry.timestamp.asc())  # type: ignore
                )
                entries = session.exec(stmt).all()
                return [
                    {
                        "id": e.id,
                        "action": e.action,
                        "user_id": e.user_id,
                        "post_id": e.post_id,
                        "details": json.loads(e.details) if e.details else {},
                        "timestamp": e.timestamp.isoformat() if e.timestamp else "",
                    }
                    for e in entries
                ]
        except Exception as e:
            logger.error("Audit retrieval failed: %s", e)
            return []

    def get_recent_activity(self, limit: int = 20) -> list[dict]:
        """Get the most recent audit entries across all campaigns."""
        try:
            with get_session() as session:
                from sqlmodel import select
                stmt = select(AuditEntry).order_by(AuditEntry.timestamp.desc()).limit(limit)  # type: ignore
                entries = session.exec(stmt).all()
                return [
                    {
                        "id": e.id,
                        "campaign_id": e.campaign_id,
                        "action": e.action,
                        "user_id": e.user_id,
                        "timestamp": e.timestamp.isoformat() if e.timestamp else "",
                    }
                    for e in entries
                ]
        except Exception as e:
            logger.error("Recent activity retrieval failed: %s", e)
            return []
