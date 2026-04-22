"""
Audience Analyzer Agent — Matches news content to the best target audience.
Outputs writing brief (for Writer) and visual style (for Image Generator).
"""
import os
import logging
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langsmith import traceable
from src.state import AgentState

logger = logging.getLogger("redm.audience")


class AudienceDecision(BaseModel):
    target_audience: str = Field(description="Audience key, e.g. 'college_students', 'general_public'.")
    audience_brief: str = Field(description="2-3 sentence writing direction: tone, focus, CTA style.")
    visual_style: str = Field(description="Short visual direction: color palette, lighting, feel. Under 25 words.")
    visual_elements: str = Field(description="ONE visual anchor from this news event. One sentence. Anonymous depictions only.")
    reasoning: str = Field(description="Brief explanation of why this audience was chosen.")


SYSTEM_PROMPT = """
You are an Audience Strategist for a Human Trafficking Awareness campaign.

Given a news story and audience profiles, you must:
1. Analyze the story — who does it affect? What domain?
2. Match to the SINGLE best audience from the profiles.
3. Output a writing brief (tone + focus + CTA).
4. Output a visual style brief (~20 words).
5. Extract ONE visual anchor — the most striking detail. One sentence.
6. ANONYMITY: Only anonymous depictions — silhouettes, hands, backs of heads. NEVER name real people.

VISUAL PHILOSOPHY — Less Is More:
- Minimalist: one subject, expansive negative space, restrained palette.
- Do NOT suggest multiple metaphors or scenes.

Rules:
- Choose the audience whose triggers BEST match the story.
- Default to "general_public" if no strong match.
"""


class AudienceAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(AudienceDecision)
        self._profiles = self._load_profiles()

    def _load_profiles(self) -> str:
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "config", "audience_profiles.md"))
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Audience profiles not found at %s", path)
            return "No profiles available. Default to general_public."

    @traceable(name="Audience Analysis")
    def analyze_audience(self, state: AgentState) -> dict:
        """Select the best target audience and produce writing + visual briefs."""
        logger.info("--- AUDIENCE ANALYZER: Matching content to audience ---")

        topic = state.get("trend_topic")
        context = state.get("trend_context")

        if not topic or not context:
            return {
                "target_audience": "general_public",
                "audience_brief": "Write for a general audience. Include the national hotline number.",
                "visual_style": "Cinematic teal-and-orange, dramatic chiaroscuro, bold typography, urban texture.",
                "visual_elements": "",
                "status": "audience_selected",
            }

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=(
                f"Story Topic: {topic}\n"
                f"Story Context: {context}\n\n"
                f"Audience Profiles Reference:\n{self._profiles}\n\n"
                f"Select the best audience and provide briefs."
            )),
        ]

        user_guidance = state.get("user_guidance")
        if user_guidance:
            messages.append(HumanMessage(content=f"USER CREATIVE DIRECTION:\n{user_guidance}"))

        decision: AudienceDecision = self.llm.invoke(messages)
        logger.info("Selected audience: %s | Reason: %s", decision.target_audience, decision.reasoning)

        return {
            "target_audience": decision.target_audience,
            "audience_brief": decision.audience_brief,
            "visual_style": decision.visual_style,
            "visual_elements": decision.visual_elements,
            "status": "audience_approved",
        }
