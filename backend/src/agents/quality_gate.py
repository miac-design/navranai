"""
Phase 11: LLM-as-Judge Quality Gate.

Scores each generated post on hallucination risk, emotional tone,
CTA clarity, and overall quality before presenting to the human reviewer.
Posts scoring below threshold are auto-regenerated (up to 2 retries).
"""
import logging
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langsmith import traceable
from src.state import AgentState, CampaignPost

logger = logging.getLogger("redm.quality_gate")

QUALITY_THRESHOLD = 6.0
MAX_RETRIES = 2


class QualityScore(BaseModel):
    overall: float = Field(description="Overall quality score 0-10")
    hallucination_risk: float = Field(description="Hallucination risk 0-10 (10 = highest risk)")
    emotional_tone: str = Field(description="appropriate | too_heavy | too_light")
    cta_clarity: float = Field(description="CTA clarity 0-10")
    source_attribution: bool = Field(description="Does the post cite a source?")
    recommendation: str = Field(description="pass | needs_revision")
    revision_notes: str = Field(default="", description="If needs_revision, explain what to fix.")


JUDGE_PROMPT = """
You are a Quality Reviewer for an anti-trafficking awareness campaign.
You review AI-generated social media posts BEFORE they reach human volunteers.

Score the post on these dimensions:

1. OVERALL (0-10): Would this post make the campaign proud?
2. HALLUCINATION RISK (0-10): Does the post contain claims not in the source?
   10 = definitely hallucinated, 0 = every claim is traceable to the source.
3. EMOTIONAL TONE: Is the tone appropriate for the content type?
   "too_heavy" = might cause compassion fatigue or re-traumatize.
   "too_light" = trivializes the issue.
   "appropriate" = balanced.
4. CTA CLARITY (0-10): Is there a clear, actionable call-to-action?
5. SOURCE ATTRIBUTION: Does the post cite where the information came from?

RECOMMENDATION:
- "pass" if overall >= 6 AND hallucination_risk <= 4 AND source_attribution is true.
- "needs_revision" otherwise. Explain what needs fixing.
"""


class QualityGate:
    def __init__(self):
        self.judge = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(QualityScore)

    @traceable(name="Quality Gate Review")
    def review_post(self, state: AgentState) -> dict:
        """Score the current post and decide if it passes quality."""
        posts = state.get("campaign_posts", [])
        idx = state.get("current_post_index", 0)

        if not posts or idx >= len(posts):
            return {"status": "error"}

        post = CampaignPost(**posts[idx])
        logger.info("--- QUALITY GATE: Reviewing %s post ---", post.content_type)

        topic = state.get("trend_topic", "")
        context = state.get("trend_context", "")
        raw_news = state.get("raw_news", [])
        source_text = "\n".join([n.get("content", "")[:3000] for n in raw_news])

        messages = [
            SystemMessage(content=JUDGE_PROMPT),
            HumanMessage(content=(
                f"CONTENT TYPE: {post.content_type}\n\n"
                f"SOURCE MATERIAL:\n{source_text[:5000]}\n\n"
                f"GENERATED POST:\n{post.caption}\n\n"
                f"Review this post."
            )),
        ]

        score: QualityScore = self.judge.invoke(messages)

        post.quality_score = score.overall
        posts[idx] = post.model_dump()

        logger.info(
            "Quality: %.1f | Hallucination: %.1f | Tone: %s | CTA: %.1f | Rec: %s",
            score.overall, score.hallucination_risk, score.emotional_tone,
            score.cta_clarity, score.recommendation,
        )

        if score.recommendation == "needs_revision" and score.overall < QUALITY_THRESHOLD:
            logger.warning("Post failed quality gate: %s", score.revision_notes)
            # The graph will handle retry logic

        return {
            "campaign_posts": posts,
            "status": "quality_checked",
        }
