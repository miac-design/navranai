"""
Phase 1: State & Data Model — Campaign-aware schema.

The AgentState now carries a list of CampaignPost objects (one per content type)
instead of a single post_text / image_path pair.
"""
import operator
from typing import Annotated, List, Optional, TypedDict
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Structured model for a single post within a 5-post campaign
# ---------------------------------------------------------------------------

class CampaignPost(BaseModel):
    """Represents one content piece in a weekly campaign."""
    content_type: str = Field(description="reactive | stat | explainer | action | hope")
    day_of_week: int = Field(default=0, description="0=Mon .. 4=Fri")
    caption: str = Field(default="")
    hashtags: list[str] = Field(default_factory=list)
    image_path: Optional[str] = Field(default=None)
    image_prompt: Optional[str] = Field(default=None)
    platform_renders: dict[str, str] = Field(default_factory=dict, description='{"ig_square": "path", ...}')
    status: str = Field(default="pending", description="pending | draft | approved | rejected")
    learning_note: Optional[str] = Field(default=None, description="Ethical language tip for this post")
    quality_score: Optional[float] = Field(default=None, description="0-10 from quality gate")
    compliance_passed: Optional[bool] = Field(default=None)
    compliance_violations: list[str] = Field(default_factory=list)
    variants: list[str] = Field(default_factory=list, description="Alternative caption options")
    cost_usd: float = Field(default=0.0)
    # Brief fields (set by campaign_planner, consumed by writer + image_gen)
    angle: str = Field(default="")
    tone: str = Field(default="")
    cta_direction: str = Field(default="")
    visual_suggestion: str = Field(default="")


# ---------------------------------------------------------------------------
# LangGraph Agent State
# ---------------------------------------------------------------------------

class AgentState(TypedDict):
    # ─── Identity ───
    campaign_id: Optional[str]

    # ─── Intelligence (from TrendAnalyzer) ───
    manual_url: Optional[str]
    story_title: Optional[str]  # Set when a story is picked from Intel → skips trend analyzer
    trend_topic: Optional[str]
    trend_context: Optional[str]
    raw_news: Optional[List[dict]]
    all_retrieved_news: Optional[List[dict]]

    # ─── Audience (from AudienceAnalyzer) ───
    target_audience: Optional[str]
    audience_brief: Optional[str]
    visual_style: Optional[str]
    visual_elements: Optional[str]
    user_guidance: Optional[str]

    # ─── Campaign Posts (from CampaignPlanner, updated by Writer/ImageGen) ───
    campaign_posts: Optional[List[dict]]  # Serialized CampaignPost dicts
    current_post_index: int

    # ─── Legacy single-post fields (kept for backward compat) ───
    writer_prompt: Optional[str]
    post_text: Optional[str]
    image_prompt: Optional[str]
    image_path: Optional[str]

    # ─── HITL Feedback ───
    feedback: Optional[str]
    image_feedback: Optional[str]
    text_feedback: Optional[str]

    # ─── Workflow ───
    status: str  # "starting" | "scanning" | "planning_campaign" | "writing" | "generating_image" |
                 # "quality_check" | "compliance_check" | "rendering" | "review" | "done" | "error"
    target_language: Optional[str]  # Phase 18: "en", "es", "fr", "pt"
