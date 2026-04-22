"""
Phase 3: Content-Type-Aware Writer Agent.

Loads per-type system prompts and generates captions tailored to each content type.
Also supports Phase 15 (content variant generation).
"""
import os
import logging
import yaml
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langsmith import traceable
from src.state import AgentState, CampaignPost

logger = logging.getLogger("redm.writer")


# ---------------------------------------------------------------------------
# Per-type system prompts (Phase 3)
# ---------------------------------------------------------------------------

TYPE_PROMPTS = {
    "reactive": """You are writing a REACTIVE (breaking news) post for an anti-trafficking awareness campaign.
FORMAT: Lead with the event. Cite the source immediately. Create urgency without panic.
STRUCTURE: HOOK (surprising fact from the news) → EDUCATE (one verified detail) → EMPOWER (one action) → SOURCE.
TONE: Authoritative, urgent, factual. Like a Reuters alert humanized.
MUST INCLUDE: Source attribution. National Hotline: 1-888-373-7888.""",

    "stat": """You are writing a STAT CARD post for an anti-trafficking awareness campaign.
FORMAT: Center ONE bold number/statistic from the source material. Make it impossible to scroll past.
STRUCTURE: THE NUMBER (big, bold) → CONTEXT (who/what in 1-2 lines) → SOURCE citation.
TONE: Data-driven, punchy, impactful. Like a NYT infographic caption.
ANTI-HALLUCINATION: If no specific number exists in the source, use a powerful qualitative statement.
MUST INCLUDE: Source attribution.""",

    "explainer": """You are writing an EXPLAINER post for an anti-trafficking awareness campaign.
FORMAT: Educational listicle. "5 Signs" or "3 Things to Know" format.
STRUCTURE: HOOK (question) → LIST (observable facts, not judgments) → CTA (learn more or share).
TONE: Calm, educational, inclusive. Like a teacher explaining to a concerned parent.
FRAMING: Signs should be observable workplace conditions, NOT racial profiling triggers.
MUST INCLUDE: National Hotline: 1-888-373-7888.""",

    "action": """You are writing an ACTION post for an anti-trafficking awareness campaign.
FORMAT: CTA-first. The entire post drives toward ONE specific action.
STRUCTURE: EMPOWERMENT HOOK → THE ACTION (call hotline, text BeFree to 233733) → WHY it matters.
TONE: Direct, empowering, barrier-lowering. "30 seconds of your time can change everything."
AVOID: Guilt-based messaging ("Don't look away"). Use empowerment ("Your voice has power").
MUST INCLUDE: 1-888-373-7888 AND TEXT BeFree to 233733.""",

    "hope": """You are writing a HOPE post for an anti-trafficking awareness campaign.
FORMAT: End-of-week positive momentum. Show that progress IS happening.
STRUCTURE: PROGRESS STAT → GRATITUDE → FORWARD-LOOKING statement.
TONE: Warm, hopeful, grateful. Like a Friday thank-you from a movement leader.
WHY: Constant crisis content causes compassion fatigue. Hope posts prevent audience disengagement.
MUST INCLUDE: Source for the positive stat. National Hotline: 1-888-373-7888.""",
}

UNIVERSAL_RULES = """
STRICT CRITERIA FOR ALL POSTS:
- ANTI-HALLUCINATION: NEVER invent numbers, statistics, names, or facts.
- Include 2-5 relevant hashtags.
- Keep under 280 characters for X compatibility (can be longer for IG).

LANGUAGE MATTERS (NEVER USE THESE):
- INSTEAD OF "Sex slave" → "Survivor of sex trafficking"
- INSTEAD OF "Child prostitute" → "Child victim of sex trafficking"
- INSTEAD OF "Rescued" → "Identified" or "Supported"
- INSTEAD OF "Sold her body" → "Was exploited" or "Was trafficked"
- INSTEAD OF "Illegal immigrant" → "Undocumented individual"
- PREFER "Survivor" over "Victim" (when person is out of situation)
"""


class WriterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        self.variant_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)  # Higher temp for variants

    def _load_language_rules(self) -> str:
        """Load language rules from YAML config."""
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "config", "content_rules.yaml"))
        try:
            with open(path, "r", encoding="utf-8") as f:
                rules = yaml.safe_load(f)
            lines = []
            for rule in rules.get("language_rules", []):
                if rule.get("enabled", True):
                    lines.append(f"- Instead of \"{rule['instead_of']}\", use \"{rule['use']}\"")
            return "\n".join(lines) if lines else ""
        except FileNotFoundError:
            return ""

    @traceable(name="Content Writing")
    def write_post(self, state: AgentState) -> dict:
        """Generate a caption for the current post in the campaign."""
        posts = state.get("campaign_posts", [])
        idx = state.get("current_post_index", 0)

        if not posts or idx >= len(posts):
            logger.error("No campaign posts or index out of range")
            return {"status": "error", "feedback": "No posts to write."}

        post = CampaignPost(**posts[idx])
        content_type = post.content_type
        logger.info("--- WRITER: Generating %s post (index %d) ---", content_type, idx)

        # Get the type-specific prompt
        type_prompt = TYPE_PROMPTS.get(content_type, TYPE_PROMPTS["reactive"])

        # Build context from state
        topic = state.get("trend_topic", "")
        context = state.get("trend_context", "")
        raw_news = state.get("raw_news", [])
        raw_texts = "\n---\n".join([
            f"Source: {n.get('url')}\nContent: {n.get('content', '')[:5000]}"
            for n in raw_news
        ])

        # Load dynamic language rules
        extra_rules = self._load_language_rules()

        system_msg = SystemMessage(content=type_prompt + "\n\n" + UNIVERSAL_RULES)
        if extra_rules:
            system_msg = SystemMessage(content=type_prompt + "\n\n" + UNIVERSAL_RULES + "\n\nADDITIONAL RULES FROM CONFIG:\n" + extra_rules)

        human_content = (
            f"Topic: {topic}\n"
            f"Context: {context}\n\n"
            f"ANGLE FOR THIS POST: {post.angle}\n"
            f"TONE: {post.tone}\n"
            f"CTA DIRECTION: {post.cta_direction}\n\n"
            f"RAW SOURCE MATERIAL:\n{raw_texts}\n\n"
            f"ANTI-HALLUCINATION: Base your post entirely on the source material above."
        )

        # Handle text feedback for regeneration
        text_feedback = state.get("text_feedback")
        if text_feedback and post.status == "rejected":
            human_content += f"\n\nUSER REWRITE INSTRUCTIONS:\n{text_feedback}"

        response = self.llm.invoke([system_msg, HumanMessage(content=human_content)])
        caption = response.content

        # Phase 15: Generate 2 additional variants
        variants = self._generate_variants(system_msg, human_content, caption)

        # Update the post
        post.caption = caption
        post.variants = variants
        post.status = "draft"
        posts[idx] = post.model_dump()

        logger.info("Written %s post: %s...", content_type, caption[:80])

        return {
            "campaign_posts": posts,
            "status": "writing",  # Will be managed by the graph loop
        }

    def _generate_variants(self, system_msg, human_content: str, primary: str) -> list[str]:
        """Phase 15: Generate 2 alternative captions."""
        try:
            variant_prompt = (
                f"{human_content}\n\n"
                f"PRIMARY CAPTION (already written):\n{primary}\n\n"
                f"Write a COMPLETELY DIFFERENT version of this post. "
                f"Same facts and structure rules, but different hook, phrasing, and emotional angle."
            )
            v1 = self.variant_llm.invoke([system_msg, HumanMessage(content=variant_prompt)]).content
            v2 = self.variant_llm.invoke([system_msg, HumanMessage(content=variant_prompt + "\nAlso different from this version:\n" + v1)]).content
            return [v1, v2]
        except Exception as e:
            logger.warning("Variant generation failed: %s", e)
            return []
