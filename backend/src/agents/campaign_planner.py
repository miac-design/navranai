"""
Phase 2: Campaign Multiplier Agent — Transforms one trend into 5 content briefs.

Takes a single news story and produces 5 structured CampaignPost briefs:
Reactive (Mon), Stat Card (Tue), Explainer (Wed), Action (Thu), Hope (Fri).
"""
import os
import logging
import yaml
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langsmith import traceable
from src.state import AgentState, CampaignPost

logger = logging.getLogger("redm.campaign_planner")


class ContentBrief(BaseModel):
    content_type: str = Field(description="One of: reactive, stat, explainer, action, hope")
    angle: str = Field(description="The specific angle/hook for this post type")
    tone: str = Field(description="Tone direction (e.g., 'urgent but factual', 'warm and hopeful')")
    cta_direction: str = Field(description="What the CTA should focus on")
    visual_suggestion: str = Field(description="One-line visual direction for image generation")
    learning_note: str = Field(description="Ethical language tip relevant to this specific post")
    caption_brief: str = Field(description="2-3 sentence draft direction for the writer")


class CampaignBriefs(BaseModel):
    briefs: list[ContentBrief] = Field(description="Exactly 5 content briefs, one per type")


SYSTEM_PROMPT = """
You are a Campaign Strategist for RedM, an anti-human-trafficking awareness organization.

Given ONE news story, you must create 5 content briefs — one for each day of the week.
Each brief targets a different content type:

MONDAY — REACTIVE: Breaking news response. Lead with the event. Urgency without panic.
TUESDAY — STAT CARD: One bold number from the story. Visual impact. Source citation mandatory.
WEDNESDAY — EXPLAINER: Educational. "5 Signs" or "3 Things to Know" format. Observable facts.
THURSDAY — ACTION: Call-to-action. Feature the hotline (1-888-373-7888) or BeFree text (233733). Empowerment.
FRIDAY — HOPE: End-of-week progress. Positive stat or momentum. "Your voice matters."

RULES:
1. Each brief MUST connect back to the original news story — do NOT invent unrelated content.
2. Each learning_note should teach one ethical language principle relevant to THAT post.
3. Visual suggestions should be specific to the content type (dark/cinematic for reactive, light/clean for stat, etc.)
4. NEVER invent statistics. If the story doesn't contain a number, suggest the writer use a qualitative statement.
5. The 5 briefs should tell a coherent week-long narrative arc: News → Data → Education → Action → Hope.
"""


class CampaignPlanner:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.3).with_structured_output(CampaignBriefs)
        self._rules = self._load_rules()

    @staticmethod
    def _load_rules() -> dict:
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "config", "content_rules.yaml"))
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning("Content rules not found at %s", path)
            return {}

    @traceable(name="Campaign Planning")
    def plan_campaign(self, state: AgentState) -> dict:
        """Transform one trend into 5 structured content briefs."""
        logger.info("--- CAMPAIGN PLANNER: Creating 5-post campaign ---")

        topic = state.get("trend_topic", "")
        context = state.get("trend_context", "")
        raw_news = state.get("raw_news", [])
        audience_brief = state.get("audience_brief", "")
        visual_style = state.get("visual_style", "")

        # Build raw source material
        raw_texts = "\n---\n".join([
            f"Source: {n.get('source')} ({n.get('url')})\nContent: {n.get('content', '')[:5000]}"
            for n in raw_news
        ])

        # Load content mix config
        mix = self._rules.get("content_mix", {})
        content_order = mix.get("order", ["reactive", "stat", "explainer", "action", "hope"])
        hotline = self._rules.get("content_rules", {}).get("hotline_number", "1-888-373-7888")

        language_rules_text = ""
        for rule in self._rules.get("language_rules", []):
            if rule.get("enabled", True):
                language_rules_text += f"- Instead of \"{rule['instead_of']}\", use \"{rule['use']}\" ({rule['reason']})\n"

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=(
                f"NEWS STORY:\n"
                f"Headline: {topic}\n"
                f"Context: {context}\n\n"
                f"RAW SOURCE MATERIAL:\n{raw_texts}\n\n"
                f"AUDIENCE BRIEF: {audience_brief}\n"
                f"VISUAL STYLE: {visual_style}\n"
                f"HOTLINE: {hotline}\n\n"
                f"ETHICAL LANGUAGE RULES:\n{language_rules_text}\n\n"
                f"Content type order: {', '.join(content_order)}\n\n"
                f"Generate exactly 5 content briefs."
            )),
        ]

        result: CampaignBriefs = self.llm.invoke(messages)

        # Convert briefs to CampaignPost objects
        campaign_posts = []
        for i, brief in enumerate(result.briefs[:5]):
            post = CampaignPost(
                content_type=brief.content_type,
                day_of_week=i,
                angle=brief.angle,
                tone=brief.tone,
                cta_direction=brief.cta_direction,
                visual_suggestion=brief.visual_suggestion,
                learning_note=brief.learning_note,
                status="pending",
            )
            campaign_posts.append(post.model_dump())

        logger.info("Campaign planned: %s", [p["content_type"] for p in campaign_posts])

        return {
            "campaign_posts": campaign_posts,
            "current_post_index": 0,
            "status": "writing",
        }
