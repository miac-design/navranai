"""
Phase 14: Prompt Registry — Version tracking and A/B testing for system prompts.

Stores prompt versions in SQLite with quality score tracking.
Enables A/B testing and prompt evolution over time.
"""
import logging
import uuid
from datetime import datetime
from typing import Optional
from src.models import PromptVersion, get_session

logger = logging.getLogger("redm.prompts")


class PromptRegistry:
    """Manages versioned system prompts for all agents."""

    def register_prompt(self, agent: str, prompt_text: str) -> str:
        """Register a new prompt version. Returns the version ID."""
        with get_session() as session:
            from sqlmodel import select

            # Get current max version for this agent
            stmt = select(PromptVersion).where(PromptVersion.agent == agent).order_by(PromptVersion.version.desc())  # type: ignore
            existing = session.exec(stmt).first()
            next_version = (existing.version + 1) if existing else 1

            # Deactivate old versions
            if existing:
                all_versions = session.exec(
                    select(PromptVersion).where(PromptVersion.agent == agent)
                ).all()
                for v in all_versions:
                    v.is_active = False
                    session.add(v)

            pv = PromptVersion(
                id=uuid.uuid4().hex[:12],
                agent=agent,
                version=next_version,
                prompt_text=prompt_text,
                created_at=datetime.utcnow(),
                is_active=True,
            )
            session.add(pv)
            session.commit()

            logger.info("Registered prompt v%d for %s", next_version, agent)
            return pv.id

    def get_active_prompt(self, agent: str) -> Optional[str]:
        """Get the currently active prompt for an agent."""
        with get_session() as session:
            from sqlmodel import select
            stmt = select(PromptVersion).where(
                PromptVersion.agent == agent,
                PromptVersion.is_active == True,  # noqa: E712
            )
            pv = session.exec(stmt).first()
            return pv.prompt_text if pv else None

    def record_quality(self, agent: str, score: float):
        """Record a quality score for the active prompt version."""
        with get_session() as session:
            from sqlmodel import select
            stmt = select(PromptVersion).where(
                PromptVersion.agent == agent,
                PromptVersion.is_active == True,  # noqa: E712
            )
            pv = session.exec(stmt).first()
            if pv:
                pv.usage_count += 1
                # Running average
                if pv.avg_quality_score is None:
                    pv.avg_quality_score = score
                else:
                    pv.avg_quality_score = (
                        (pv.avg_quality_score * (pv.usage_count - 1) + score) / pv.usage_count
                    )
                session.add(pv)
                session.commit()

    def get_all_versions(self, agent: str) -> list[dict]:
        """Get all versions for an agent, for A/B comparison."""
        with get_session() as session:
            from sqlmodel import select
            stmt = select(PromptVersion).where(PromptVersion.agent == agent).order_by(PromptVersion.version.desc())  # type: ignore
            versions = session.exec(stmt).all()
            return [
                {
                    "id": v.id,
                    "version": v.version,
                    "is_active": v.is_active,
                    "avg_quality_score": v.avg_quality_score,
                    "usage_count": v.usage_count,
                    "created_at": v.created_at.isoformat() if v.created_at else "",
                }
                for v in versions
            ]
