"""
Phase 1: SQLModel persistence layer.

Provides Campaign, Post, IntelStory, AuditEntry, PromptVersion, and CostLog tables.
Uses SQLite — zero-setup, ships as a single file.
"""
import uuid
import json
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session
from config import DATABASE_URL

import logging
logger = logging.getLogger("redm.models")


# ---------------------------------------------------------------------------
# Table Definitions
# ---------------------------------------------------------------------------

class Campaign(SQLModel, table=True):
    """A weekly content campaign derived from one intelligence story."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12], primary_key=True)
    source_url: str = Field(default="")
    source_title: str = Field(default="")
    source_snippet: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="generating")  # generating | review | approved | published
    total_cost_usd: float = Field(default=0.0)
    language: str = Field(default="en")
    thread_id: str = Field(default="")  # LangGraph thread reference


class Post(SQLModel, table=True):
    """A single content piece within a campaign."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12], primary_key=True)
    campaign_id: str = Field(default="", index=True)
    content_type: str = Field(default="")  # reactive | stat | explainer | action | hope
    day_of_week: int = Field(default=0)
    caption: str = Field(default="")
    hashtags: str = Field(default="[]")  # JSON-serialized list
    image_path: str = Field(default="")
    image_prompt: str = Field(default="")
    platform_renders: str = Field(default="{}")  # JSON dict
    quality_score: float = Field(default=0.0)
    compliance_passed: bool = Field(default=False)
    compliance_violations: str = Field(default="[]")  # JSON list
    variants: str = Field(default="[]")  # JSON list of alt captions
    cost_usd: float = Field(default=0.0)
    learning_note: str = Field(default="")
    status: str = Field(default="draft")  # draft | approved | rejected
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class IntelStory(SQLModel, table=True):
    """A scanned news story from the intelligence feed."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12], primary_key=True)
    title: str = Field(default="")
    source: str = Field(default="")
    url: str = Field(default="", index=True)
    snippet: str = Field(default="")
    full_content: str = Field(default="")
    relevance_score: float = Field(default=0.0)
    is_ai_pick: bool = Field(default=False)
    scanned_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = Field(default=None)
    used_in_campaign_id: Optional[str] = Field(default=None)


class AuditEntry(SQLModel, table=True):
    """Phase 19: Tracks every action for accountability."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12], primary_key=True)
    campaign_id: str = Field(default="", index=True)
    post_id: Optional[str] = Field(default=None)
    action: str = Field(default="")  # created | edited | approved | rejected | regenerated | compliance_flagged
    user_id: str = Field(default="system")
    details: str = Field(default="{}")  # JSON — what changed
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PromptVersion(SQLModel, table=True):
    """Phase 14: Tracks prompt versions for A/B testing."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12], primary_key=True)
    agent: str = Field(default="")  # writer_reactive, writer_stat, etc.
    version: int = Field(default=1)
    prompt_text: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    avg_quality_score: Optional[float] = Field(default=None)
    usage_count: int = Field(default=0)
    is_active: bool = Field(default=True)


class CostLog(SQLModel, table=True):
    """Phase 13: Token-level API cost logging."""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12], primary_key=True)
    campaign_id: str = Field(default="", index=True)
    agent: str = Field(default="")
    model: str = Field(default="")
    input_tokens: int = Field(default=0)
    output_tokens: int = Field(default=0)
    cost_usd: float = Field(default=0.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Database Engine & Init
# ---------------------------------------------------------------------------

engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    """Create all tables if they don't exist."""
    SQLModel.metadata.create_all(engine)
    logger.info("Database initialized at %s", DATABASE_URL)


def get_session() -> Session:
    """Get a new database session."""
    return Session(engine)
