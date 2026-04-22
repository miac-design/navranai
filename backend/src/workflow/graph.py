"""
Phase 6: Graph Workflow Rewrite.

New flow:
  START → route_entry → [trend_analyzer OR story_loader] → audience_analyzer → campaign_planner →
  [LOOP 5 posts]: writer → quality_gate → compliance_check → image_gen → renderer
  → INTERRUPT (batch review) → END

When a story is pre-selected from the Intelligence page, trend_analyzer is SKIPPED.
The story_loader directly populates trend state from the selected story.
"""
import logging
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents.trend_analyzer import TrendAnalyzer
from src.agents.audience_analyzer import AudienceAnalyzer
from src.agents.campaign_planner import CampaignPlanner
from src.agents.writer import WriterAgent
from src.agents.image_generator import ImageGeneratorAgent
from src.agents.quality_gate import QualityGate
from src.agents.compliance_checker import ComplianceChecker
from src.tools.platform_renderer import PlatformRenderer
from src.tools.crawl4ai_scraper import Crawl4AIScraper

logger = logging.getLogger("redm.graph")


def create_graph():
    """Build and compile the V3 campaign generation graph."""

    # Initialize all agents
    trend_analyzer = TrendAnalyzer()
    audience_analyzer = AudienceAnalyzer()
    campaign_planner = CampaignPlanner()
    writer = WriterAgent()
    image_gen = ImageGeneratorAgent()
    quality_gate = QualityGate()
    compliance = ComplianceChecker()
    renderer = PlatformRenderer()

    # -- Story loader: bypasses trend analyzer when story is pre-selected --

    def load_story(state: AgentState) -> dict:
        """
        When a user picks a story from the Intel page, the story URL is passed
        as manual_url AND story_title is set. This node scrapes the article
        and populates the trend state directly — NO LLM call needed.
        """
        url = state.get("manual_url", "")
        title = state.get("story_title", "Selected Article")
        logger.info("--- STORY LOADER: Bypassing trend analyzer for: %s ---", url)

        content = ""
        try:
            scraper = Crawl4AIScraper()
            content = scraper.read_url(url)
        except Exception as e:
            logger.error("Failed to scrape story URL: %s", e)

        # Truncate for downstream safety
        content_truncated = content[:4000] if content else ""

        return {
            "trend_topic": title,
            "trend_context": content_truncated,
            "raw_news": [{"title": title, "source": "Intel Feed", "url": url, "content": content}],
            "all_retrieved_news": [{"title": title, "source": "Intel Feed", "url": url, "content": content}],
            "writer_prompt": None,
            "visual_style": None,
            "post_text": None,
            "image_path": None,
            "campaign_posts": None,
            "current_post_index": 0,
            "status": "planning",
        }

    # -- Wrapper nodes that handle loop logic --

    def write_current_post(state: AgentState) -> dict:
        """Write the caption for the current post index."""
        return writer.write_post(state)

    def check_quality(state: AgentState) -> dict:
        """Quality gate for the current post."""
        return quality_gate.review_post(state)

    def check_compliance(state: AgentState) -> dict:
        """Compliance check for the current post."""
        return compliance.check_compliance(state)

    def generate_image_current(state: AgentState) -> dict:
        """Generate image for the current post."""
        return image_gen.generate_image(state)

    def render_platforms(state: AgentState) -> dict:
        """Render current post into platform sizes."""
        return renderer.render_platforms(state)

    def advance_post_index(state: AgentState) -> dict:
        """Move to the next post in the campaign."""
        idx = state.get("current_post_index", 0)
        posts = state.get("campaign_posts", [])
        next_idx = idx + 1
        logger.info("Post %d/%d complete → advancing to %d", idx + 1, len(posts), next_idx + 1)
        return {"current_post_index": next_idx, "status": "writing"}

    def mark_review(state: AgentState) -> dict:
        """All 5 posts generated — ready for human batch review."""
        logger.info("All posts generated — entering batch review")
        return {"status": "review"}

    # -- Routing functions --

    def route_entry(state: AgentState) -> str:
        """
        Entry router: if a story is already selected (story_title is set),
        skip trend analysis entirely and load the story directly.
        """
        if state.get("story_title"):
            logger.info("Story pre-selected — skipping trend analyzer")
            return "story_loader"
        return "trend_analyzer"

    def route_after_planner(state: AgentState) -> str:
        """After campaign planning, start writing."""
        posts = state.get("campaign_posts")
        if not posts:
            return "FINISH"
        return "write_post"

    def route_after_render(state: AgentState) -> str:
        """After rendering, decide: loop to next post or go to review."""
        idx = state.get("current_post_index", 0)
        posts = state.get("campaign_posts", [])
        if idx + 1 < len(posts):
            return "advance"
        else:
            return "review"

    # -- Build the graph --
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("entry_router", lambda state: {})  # no-op decision node
    workflow.add_node("trend_analyzer", trend_analyzer.analyze_trends)
    workflow.add_node("story_loader", load_story)
    workflow.add_node("audience_analyzer", audience_analyzer.analyze_audience)
    workflow.add_node("campaign_planner", campaign_planner.plan_campaign)
    workflow.add_node("write_post", write_current_post)
    workflow.add_node("quality_gate", check_quality)
    workflow.add_node("compliance_check", check_compliance)
    workflow.add_node("image_generator", generate_image_current)
    workflow.add_node("platform_renderer", render_platforms)
    workflow.add_node("advance_index", advance_post_index)
    workflow.add_node("batch_review", mark_review)

    # Entry: route to trend_analyzer OR story_loader
    workflow.set_entry_point("entry_router")
    workflow.add_conditional_edges(
        "entry_router",
        route_entry,
        {"trend_analyzer": "trend_analyzer", "story_loader": "story_loader"},
    )

    # Both paths converge at audience_analyzer
    workflow.add_edge("trend_analyzer", "audience_analyzer")
    workflow.add_edge("story_loader", "audience_analyzer")
    workflow.add_edge("audience_analyzer", "campaign_planner")

    # After planning: conditional start
    workflow.add_conditional_edges(
        "campaign_planner",
        route_after_planner,
        {"write_post": "write_post", "FINISH": END},
    )

    # Per-post pipeline: write → quality → compliance → image → render
    workflow.add_edge("write_post", "quality_gate")
    workflow.add_edge("quality_gate", "compliance_check")
    workflow.add_edge("compliance_check", "image_generator")
    workflow.add_edge("image_generator", "platform_renderer")

    # After render: loop or review
    workflow.add_conditional_edges(
        "platform_renderer",
        route_after_render,
        {"advance": "advance_index", "review": "batch_review"},
    )

    # Advance loops back to writer
    workflow.add_edge("advance_index", "write_post")

    # Review → end
    workflow.add_edge("batch_review", END)

    # Compile with checkpointer
    from langgraph.checkpoint.memory import MemorySaver
    memory = MemorySaver()

    app = workflow.compile(
        checkpointer=memory,
        interrupt_after=["batch_review"],
    )

    logger.info("V3 graph compiled: 12 nodes, 5-post campaign loop (with story bypass)")
    return app
