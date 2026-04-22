"""
Phase 13: Cost Tracker.

Logs every LLM API call's token usage and computes cost.
Stores in SQLite, queryable per campaign.
"""
import logging
import uuid
from datetime import datetime
from src.models import CostLog, get_session

logger = logging.getLogger("redm.cost")


# Pricing per 1M tokens (as of 2026)
PRICING = {
    "gpt-4o":         {"input": 2.50,  "output": 10.00},
    "gpt-4o-mini":    {"input": 0.15,  "output": 0.60},
    "gemini-flash":   {"input": 0.0,   "output": 0.0},
    "gemini-3.1-flash-image-preview": {"input": 0.0, "output": 0.0},
}


class CostTracker:
    """Tracks API costs per campaign and agent."""

    def log_call(
        self,
        campaign_id: str,
        agent: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        """Log an API call and return its cost in USD."""
        pricing = PRICING.get(model, {"input": 0.0, "output": 0.0})
        cost = (input_tokens * pricing["input"] / 1_000_000) + (output_tokens * pricing["output"] / 1_000_000)

        try:
            with get_session() as session:
                entry = CostLog(
                    id=uuid.uuid4().hex[:12],
                    campaign_id=campaign_id,
                    agent=agent,
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost_usd=round(cost, 6),
                    timestamp=datetime.utcnow(),
                )
                session.add(entry)
                session.commit()
        except Exception as e:
            logger.error("Failed to log cost: %s", e)

        return cost

    def get_campaign_cost(self, campaign_id: str) -> dict:
        """Get total cost breakdown for a campaign."""
        try:
            with get_session() as session:
                from sqlmodel import select
                stmt = select(CostLog).where(CostLog.campaign_id == campaign_id)
                logs = session.exec(stmt).all()

                total = sum(l.cost_usd for l in logs)
                by_agent = {}
                for log in logs:
                    by_agent.setdefault(log.agent, 0.0)
                    by_agent[log.agent] += log.cost_usd

                return {
                    "campaign_id": campaign_id,
                    "total_usd": round(total, 4),
                    "by_agent": {k: round(v, 4) for k, v in by_agent.items()},
                    "call_count": len(logs),
                }
        except Exception as e:
            logger.error("Failed to get campaign cost: %s", e)
            return {"total_usd": 0.0, "by_agent": {}, "call_count": 0}

    def get_total_cost(self) -> float:
        """Get lifetime total cost across all campaigns."""
        try:
            with get_session() as session:
                from sqlmodel import select
                logs = session.exec(select(CostLog)).all()
                return round(sum(l.cost_usd for l in logs), 4)
        except Exception:
            return 0.0
