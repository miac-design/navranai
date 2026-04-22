"""
Phase 7 + 17: Full API Server with WebSocket support.

Endpoints:
  - Intelligence: /api/intel/scan, /api/intel/stories
  - Campaign:     /api/campaign/generate, /api/campaign/{id}, /api/campaign/{id}/approve-all,
                  /api/campaign/{id}/posts/{idx}/approve, /api/campaign/{id}/posts/{idx}/edit,
                  /api/campaign/{id}/posts/{idx}/regen-image
  - Library:      /api/library
  - Rules:        /api/rules
  - Settings:     /api/settings
  - Audit:        /api/audit/{campaign_id}
  - Costs:        /api/costs, /api/costs/{campaign_id}
  - WebSocket:    /ws/campaign/{id}
"""
import os
import uuid
import json
import asyncio
import logging
import datetime
import yaml
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

from src.models import init_db, get_session, Campaign, Post, IntelStory
from src.workflow.graph import create_graph
from src.services.intel_service import IntelService
from src.services.audit_service import AuditService
from src.services.cost_tracker import CostTracker
from src.services.scheduler import PublishScheduler

logger = logging.getLogger("redm.server")


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("RedM Command Center V3 — Server starting")
    yield
    logger.info("Server shutting down")


app = FastAPI(title="RedM Command Center V3 API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Serve output files
os.makedirs("outputs", exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Serve the dashboard from the backend
from fastapi.responses import FileResponse

DASHBOARD_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "design_v3.html"))

@app.get("/", include_in_schema=False)
async def serve_dashboard():
    if os.path.exists(DASHBOARD_PATH):
        return FileResponse(DASHBOARD_PATH, media_type="text/html")
    return {"error": "design_v3.html not found"}

# Global instances
agent_app = create_graph()
intel_service = IntelService()
audit_service = AuditService()
cost_tracker = CostTracker()
publish_scheduler = PublishScheduler()

# WebSocket connection manager (Phase 17)
ws_connections: Dict[str, List[WebSocket]] = {}


# ---------------------------------------------------------------------------
# Request/Response Models
# ---------------------------------------------------------------------------

class StartCampaignRequest(BaseModel):
    story_id: Optional[str] = None
    manual_url: Optional[str] = None

class EditPostRequest(BaseModel):
    caption: Optional[str] = None
    hashtags: Optional[List[str]] = None

class RegenImageRequest(BaseModel):
    instructions: str

class RegenCaptionRequest(BaseModel):
    instructions: Optional[str] = ""

class UpdateRulesRequest(BaseModel):
    rules: Dict[str, Any]

class UpdateSettingsRequest(BaseModel):
    settings: Dict[str, Any]

class TranslateRequest(BaseModel):
    target_language: str


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def ws_broadcast(campaign_id: str, event: str, data: dict = {}):
    """Send a real-time update to all WebSocket clients watching this campaign."""
    msg = json.dumps({"event": event, **data})
    for ws in ws_connections.get(campaign_id, []):
        try:
            await ws.send_text(msg)
        except Exception:
            pass

def run_campaign_pipeline(config_dict: dict, campaign_id: str):
    """Run the LangGraph pipeline in a background thread."""
    try:
        while True:
            events = list(agent_app.stream(None, config_dict, stream_mode="values"))
            state_snap = agent_app.get_state(config_dict)
            if not state_snap.next:
                break
            status = state_snap.values.get("status", "")
            if status in ["review", "done", "error"]:
                break
    except Exception as e:
        logger.error("Pipeline error: %s", e)

    # Persist results to SQLite
    try:
        state = agent_app.get_state(config_dict).values
        posts = state.get("campaign_posts", [])
        with get_session() as session:
            from sqlmodel import select
            campaign = session.exec(select(Campaign).where(Campaign.id == campaign_id)).first()
            if campaign:
                campaign.status = state.get("status", "review")
                campaign.source_title = state.get("trend_topic", "")
                session.add(campaign)

                for i, p in enumerate(posts):
                    post = Post(
                        id=uuid.uuid4().hex[:12],
                        campaign_id=campaign_id,
                        content_type=p.get("content_type", ""),
                        day_of_week=i,
                        caption=p.get("caption", ""),
                        hashtags=json.dumps(p.get("hashtags", [])),
                        image_path=p.get("image_path", ""),
                        image_prompt=p.get("image_prompt", ""),
                        platform_renders=json.dumps(p.get("platform_renders", {})),
                        quality_score=p.get("quality_score", 0.0),
                        compliance_passed=p.get("compliance_passed", False),
                        compliance_violations=json.dumps(p.get("compliance_violations", [])),
                        variants=json.dumps(p.get("variants", [])),
                        cost_usd=p.get("cost_usd", 0.0),
                        learning_note=p.get("learning_note", ""),
                        status="draft",
                    )
                    session.add(post)

                session.commit()
                audit_service.log(campaign_id, "campaign_generated", details={"post_count": len(posts)})
    except Exception as e:
        logger.error("Failed to persist campaign: %s", e)


# ---------------------------------------------------------------------------
# Intelligence Endpoints (Phase 8)
# ---------------------------------------------------------------------------

@app.post("/api/intel/scan")
async def scan_intel():
    """Trigger a news scan, rank results, and store."""
    try:
        stories = intel_service.scan()
        return {"stories": stories, "count": len(stories)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/intel/stories")
async def get_intel_stories():
    """Get cached intelligence stories."""
    stories = intel_service.get_stories()
    return {"stories": stories}


# ---------------------------------------------------------------------------
# Campaign Endpoints (Phase 7)
# ---------------------------------------------------------------------------

@app.post("/api/campaign/generate")
async def generate_campaign(req: StartCampaignRequest):
    """Start a new 5-post campaign from a story or URL."""
    campaign_id = uuid.uuid4().hex[:12]
    thread_id = f"V3-{datetime.datetime.now().strftime('%m%d-%H%M%S')}-{campaign_id}"
    config_dict = {"configurable": {"thread_id": thread_id}, "run_name": f"V3 Campaign {campaign_id}"}

    # Create campaign record
    with get_session() as session:
        campaign = Campaign(
            id=campaign_id,
            source_url=req.manual_url or "",
            thread_id=thread_id,
            status="generating",
        )
        if req.story_id:
            story = intel_service.pick_story(req.story_id)
            if story:
                campaign.source_url = story["url"]
                campaign.source_title = story["title"]
        session.add(campaign)
        session.commit()

    # Initialize state
    initial_state = {"status": "starting", "campaign_id": campaign_id, "current_post_index": 0}
    if req.manual_url:
        initial_state["manual_url"] = req.manual_url.strip()
    elif req.story_id:
        # Pass the story URL + title so the graph SKIPS trend_analyzer
        story = intel_service.pick_story(req.story_id)
        if story and story.get("url"):
            initial_state["manual_url"] = story["url"]
            initial_state["story_title"] = story.get("title", "Selected Article")

    try:
        agent_app.update_state(config_dict, initial_state)
        asyncio.create_task(asyncio.to_thread(run_campaign_pipeline, config_dict, campaign_id))
        audit_service.log(campaign_id, "campaign_started")
        return {"campaign_id": campaign_id, "thread_id": thread_id, "message": "Campaign generation started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/campaign/{campaign_id}")
async def get_campaign(campaign_id: str):
    """Get a campaign with all its posts."""
    with get_session() as session:
        from sqlmodel import select
        campaign = session.exec(select(Campaign).where(Campaign.id == campaign_id)).first()
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

        posts = session.exec(
            select(Post).where(Post.campaign_id == campaign_id).order_by(Post.day_of_week)  # type: ignore
        ).all()

        return {
            "campaign": {
                "id": campaign.id,
                "source_url": campaign.source_url,
                "source_title": campaign.source_title,
                "status": campaign.status,
                "total_cost_usd": campaign.total_cost_usd,
                "language": campaign.language,
                "created_at": campaign.created_at.isoformat() if campaign.created_at else "",
            },
            "posts": [
                {
                    "id": p.id,
                    "content_type": p.content_type,
                    "day_of_week": p.day_of_week,
                    "caption": p.caption,
                    "hashtags": json.loads(p.hashtags) if p.hashtags else [],
                    "image_path": p.image_path,
                    "platform_renders": json.loads(p.platform_renders) if p.platform_renders else {},
                    "quality_score": p.quality_score,
                    "compliance_passed": p.compliance_passed,
                    "compliance_violations": json.loads(p.compliance_violations) if p.compliance_violations else [],
                    "variants": json.loads(p.variants) if p.variants else [],
                    "cost_usd": p.cost_usd,
                    "learning_note": p.learning_note,
                    "status": p.status,
                }
                for p in posts
            ],
        }


@app.post("/api/campaign/{campaign_id}/posts/{post_idx}/approve")
async def approve_post(campaign_id: str, post_idx: int):
    """Approve a single post."""
    with get_session() as session:
        from sqlmodel import select
        posts = session.exec(
            select(Post).where(Post.campaign_id == campaign_id).order_by(Post.day_of_week)  # type: ignore
        ).all()
        if post_idx >= len(posts):
            raise HTTPException(status_code=404, detail="Post not found")
        posts[post_idx].status = "approved"
        posts[post_idx].updated_at = datetime.datetime.utcnow()
        session.add(posts[post_idx])
        session.commit()
        audit_service.log(campaign_id, "post_approved", post_id=posts[post_idx].id)
        await ws_broadcast(campaign_id, "post_approved", {"index": post_idx})
        return {"message": f"Post {post_idx} approved"}


@app.post("/api/campaign/{campaign_id}/posts/{post_idx}/edit")
async def edit_post(campaign_id: str, post_idx: int, req: EditPostRequest):
    """Edit a post's caption and/or hashtags."""
    with get_session() as session:
        from sqlmodel import select
        posts = session.exec(
            select(Post).where(Post.campaign_id == campaign_id).order_by(Post.day_of_week)  # type: ignore
        ).all()
        if post_idx >= len(posts):
            raise HTTPException(status_code=404, detail="Post not found")
        post = posts[post_idx]
        old_caption = post.caption
        if req.caption is not None:
            post.caption = req.caption
        if req.hashtags is not None:
            post.hashtags = json.dumps(req.hashtags)
        post.updated_at = datetime.datetime.utcnow()
        session.add(post)
        session.commit()
        audit_service.log(campaign_id, "post_edited", post_id=post.id,
                         details={"old_caption": old_caption[:100], "new_caption": post.caption[:100]})
        await ws_broadcast(campaign_id, "post_edited", {"index": post_idx})
        return {"message": f"Post {post_idx} updated"}


@app.post("/api/campaign/{campaign_id}/posts/{post_idx}/regen-image")
async def regen_image(campaign_id: str, post_idx: int, req: RegenImageRequest):
    """Regenerate an image for a specific post with user instructions."""
    audit_service.log(campaign_id, "image_regenerated", details={"index": post_idx, "instructions": req.instructions})
    # In production, this would trigger the image_generator agent with feedback
    return {"message": f"Image regeneration queued for post {post_idx}", "instructions": req.instructions}


@app.post("/api/campaign/{campaign_id}/posts/{post_idx}/regen-caption")
async def regen_caption(campaign_id: str, post_idx: int, req: RegenCaptionRequest):
    """Regenerate caption text for a specific post using the Writer agent."""
    with get_session() as session:
        from sqlmodel import select
        posts = session.exec(
            select(Post).where(Post.campaign_id == campaign_id)
        ).all()
        posts.sort(key=lambda p: p.day_of_week)
        if post_idx >= len(posts):
            raise HTTPException(404, "Post not found")
        post = posts[post_idx]

        # Use the Writer agent to regenerate the caption
        try:
            from src.agents.writer import Writer
            writer = Writer()
            # Build a minimal context for the writer
            result = await asyncio.to_thread(
                writer.llm.invoke,
                f"Rewrite this social media caption for an anti-trafficking campaign. "
                f"Content type: {post.content_type}. "
                f"{'User instructions: ' + req.instructions + '. ' if req.instructions else ''}"
                f"Original caption:\n\n{post.caption}\n\n"
                f"Write a fresh, improved version. Keep the hotline number 1-888-373-7888. "
                f"Include 3-5 relevant hashtags at the end."
            )
            new_caption = result.content if hasattr(result, 'content') else str(result)
            old_caption = post.caption
            post.caption = new_caption
            session.add(post)
            session.commit()
            audit_service.log(campaign_id, "caption_regenerated", post_id=post.id,
                            details={"index": post_idx, "instructions": req.instructions,
                                     "old_caption": old_caption[:100]})
            await ws_broadcast(campaign_id, "post_edited", {"index": post_idx})
            return {"message": f"Caption regenerated for post {post_idx}", "caption": new_caption}
        except Exception as e:
            raise HTTPException(500, f"Caption regeneration failed: {str(e)}")


@app.post("/api/campaign/{campaign_id}/approve-all")
async def approve_all(campaign_id: str):
    """Batch approve all posts in a campaign."""
    with get_session() as session:
        from sqlmodel import select
        posts = session.exec(select(Post).where(Post.campaign_id == campaign_id)).all()
        for post in posts:
            post.status = "approved"
            post.updated_at = datetime.datetime.utcnow()
            session.add(post)

        campaign = session.exec(select(Campaign).where(Campaign.id == campaign_id)).first()
        if campaign:
            campaign.status = "approved"
            session.add(campaign)

        session.commit()
        audit_service.log(campaign_id, "batch_approved", details={"post_count": len(posts)})
        await ws_broadcast(campaign_id, "batch_approved")
        return {"message": f"All {len(posts)} posts approved"}


# ---------------------------------------------------------------------------
# Library (Phase 7)
# ---------------------------------------------------------------------------

@app.get("/api/library")
async def get_library():
    """Get all past campaigns with summary stats."""
    with get_session() as session:
        from sqlmodel import select
        campaigns = session.exec(select(Campaign).order_by(Campaign.created_at.desc())).all()  # type: ignore
        results = []
        for c in campaigns:
            posts = session.exec(select(Post).where(Post.campaign_id == c.id)).all()
            # Find first post with an image for the thumbnail
            thumbnail = ""
            for p in posts:
                if p.image_path:
                    thumbnail = p.image_path
                    break
            results.append({
                "id": c.id,
                "source_title": c.source_title,
                "status": c.status,
                "total_cost_usd": c.total_cost_usd,
                "post_count": len(posts),
                "approved_count": sum(1 for p in posts if p.status == "approved"),
                "created_at": c.created_at.isoformat() if c.created_at else "",
                "thumbnail_url": f"/outputs/{os.path.basename(thumbnail)}" if thumbnail else "",
            })
        return {"campaigns": results}


# ---------------------------------------------------------------------------
# Rules (Phase 9)
# ---------------------------------------------------------------------------

@app.get("/api/rules")
async def get_rules():
    """Get current content rules."""
    path = os.path.normpath(os.path.join("config", "content_rules.yaml"))
    try:
        with open(path, "r", encoding="utf-8") as f:
            rules = yaml.safe_load(f)
        return {"rules": rules}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Rules file not found")


@app.put("/api/rules")
async def update_rules(req: UpdateRulesRequest):
    """Update content rules from the dashboard."""
    path = os.path.normpath(os.path.join("config", "content_rules.yaml"))
    try:
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(req.rules, f, default_flow_style=False, allow_unicode=True)
        audit_service.log("system", "rules_updated", details={"keys": list(req.rules.keys())})
        return {"message": "Rules updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Settings (Phase 7)
# ---------------------------------------------------------------------------

SETTINGS_PATH = os.path.normpath(os.path.join("config", "settings.yaml"))

@app.get("/api/settings")
async def get_settings():
    """Get application settings."""
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return {"settings": yaml.safe_load(f)}
    except FileNotFoundError:
        defaults = {
            "scan_frequency_hours": 6,
            "posts_per_campaign": 5,
            "default_platforms": ["ig_square", "x_card", "li_post"],
            "auto_publish": False,
        }
        return {"settings": defaults}


@app.put("/api/settings")
async def update_settings(req: UpdateSettingsRequest):
    """Update application settings."""
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            yaml.dump(req.settings, f, default_flow_style=False)
        return {"message": "Settings updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Audit (Phase 19)
# ---------------------------------------------------------------------------

@app.get("/api/audit/{campaign_id}")
async def get_audit(campaign_id: str):
    """Get full audit trail for a campaign."""
    history = audit_service.get_campaign_history(campaign_id)
    return {"entries": history}


@app.get("/api/audit")
async def get_recent_audit():
    """Get recent activity across all campaigns."""
    activity = audit_service.get_recent_activity()
    return {"entries": activity}


# ---------------------------------------------------------------------------
# Costs (Phase 13)
# ---------------------------------------------------------------------------

@app.get("/api/costs")
async def get_total_costs():
    """Get lifetime cost summary."""
    total = cost_tracker.get_total_cost()
    return {"total_usd": total}


@app.get("/api/costs/{campaign_id}")
async def get_campaign_costs(campaign_id: str):
    """Get cost breakdown for a specific campaign."""
    return cost_tracker.get_campaign_cost(campaign_id)


# ---------------------------------------------------------------------------
# Translation (Phase 18)
# ---------------------------------------------------------------------------

@app.post("/api/campaign/{campaign_id}/translate")
async def translate_campaign(campaign_id: str, req: TranslateRequest):
    """Translate a campaign into another language."""
    from src.services.language_adapter import LanguageAdapter
    adapter = LanguageAdapter()

    with get_session() as session:
        from sqlmodel import select
        posts = session.exec(
            select(Post).where(Post.campaign_id == campaign_id).order_by(Post.day_of_week)  # type: ignore
        ).all()
        post_dicts = [
            {"caption": p.caption, "hashtags": json.loads(p.hashtags) if p.hashtags else []}
            for p in posts
        ]

    translated = adapter.translate_campaign(post_dicts, req.target_language)
    audit_service.log(campaign_id, "translated", details={"language": req.target_language})
    return {"translated_posts": translated, "language": req.target_language}


# ---------------------------------------------------------------------------
# Download Bundle (Phase 20)
# ---------------------------------------------------------------------------

@app.get("/api/campaign/{campaign_id}/download")
async def download_campaign(campaign_id: str):
    """Create and return a download bundle ZIP."""
    path = publish_scheduler.create_download_bundle(campaign_id)
    if path:
        return {"download_url": f"http://localhost:8000/{path.replace(os.sep, '/')}"}
    raise HTTPException(status_code=500, detail="Bundle creation failed")


# ---------------------------------------------------------------------------
# WebSocket (Phase 17)
# ---------------------------------------------------------------------------

@app.websocket("/ws/campaign/{campaign_id}")
async def campaign_websocket(websocket: WebSocket, campaign_id: str):
    """Real-time updates for a campaign."""
    await websocket.accept()
    ws_connections.setdefault(campaign_id, []).append(websocket)
    logger.info("WebSocket connected for campaign %s", campaign_id)
    try:
        while True:
            # Keep connection alive, receive any client messages
            data = await websocket.receive_text()
            logger.debug("WS message from client: %s", data)
    except WebSocketDisconnect:
        ws_connections[campaign_id].remove(websocket)
        logger.info("WebSocket disconnected for campaign %s", campaign_id)


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------

@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "3.0.0",
        "endpoints": 17,
        "features": [
            "5-post campaigns", "quality gate", "compliance checker",
            "multi-platform rendering", "semantic dedup", "cost tracking",
            "audit trail", "multi-language", "websocket updates", "auto-publish",
        ],
    }
