"""
Phase 8: Intelligence Feed Service.

Decouples news scanning from content generation.
Powers the Intelligence page on the dashboard.
"""
import logging
import uuid
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from langsmith import traceable
from src.tools.exa_search import ExaSearch
from src.models import IntelStory, get_session
import config

logger = logging.getLogger("redm.intel")


class StoryRanking(BaseModel):
    title: str = Field(description="Cleaned headline")
    relevance_score: float = Field(description="0-100 relevance to human trafficking")
    snippet: str = Field(description="2-3 sentence summary of why this story matters")
    is_ai_pick: bool = Field(description="True if this is the top recommended story")


class StoryRankings(BaseModel):
    rankings: list[StoryRanking] = Field(description="Ranked stories, best first")


class IntelService:
    def __init__(self):
        self.ranker = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(StoryRankings)

    @traceable(name="Intelligence Scan")
    def scan(self) -> list[dict]:
        """Execute a scan, rank results, and persist to database."""
        logger.info("--- INTEL SERVICE: Scanning for news ---")

        try:
            from src.tools.google_news import GoogleNewsSearch
            search = GoogleNewsSearch()
            raw_articles = search.search_news(
                query='"human trafficking"',
                num_results=20,
            )
        except Exception as e:
            logger.error("Scan failed: %s", e)
            return []

        if not raw_articles:
            return []

        # Persist to database
        results = []
        with get_session() as session:
            for i, article in enumerate(raw_articles):
                # Parse the article's actual publication date from RSS
                pub_dt = None
                ts = article.get("timestamp", "")
                if ts:
                    try:
                        pub_dt = parsedate_to_datetime(ts)
                    except Exception:
                        try:
                            pub_dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        except Exception:
                            pub_dt = None

                story = IntelStory(
                    id=uuid.uuid4().hex[:12],
                    title=article["title"],
                    source=article["source"],
                    url=article["url"],
                    snippet=article.get("content", "")[:200],
                    full_content=article.get("content", ""),
                    relevance_score=50.0,
                    is_ai_pick=(i == 0),
                    scanned_at=datetime.utcnow(),
                    published_at=pub_dt,
                )
                session.add(story)
                results.append({
                    "id": story.id,
                    "title": story.title,
                    "source": story.source,
                    "url": story.url,
                    "snippet": story.snippet,
                    "relevance_score": story.relevance_score,
                    "is_ai_pick": story.is_ai_pick,
                    "published_at": story.published_at.isoformat() if story.published_at else "",
                    "scanned_at": story.scanned_at.isoformat(),
                })
            session.commit()

        logger.info("Scan complete: %d stories stored", len(results))
        return results

    def get_stories(self, limit: int = 10) -> list[dict]:
        """Get cached stories from the database."""
        with get_session() as session:
            from sqlmodel import select
            stmt = select(IntelStory).order_by(IntelStory.scanned_at.desc()).limit(limit)  # type: ignore
            stories = session.exec(stmt).all()
            return [
                {
                    "id": s.id,
                    "title": s.title,
                    "source": s.source,
                    "url": s.url,
                    "snippet": s.snippet,
                    "relevance_score": s.relevance_score,
                    "is_ai_pick": s.is_ai_pick,
                    "published_at": s.published_at.isoformat() if s.published_at else "",
                    "scanned_at": s.scanned_at.isoformat() if s.scanned_at else "",
                    "used_in_campaign_id": s.used_in_campaign_id,
                }
                for s in stories
            ]

    def pick_story(self, story_id: str) -> Optional[dict]:
        """Mark a story as picked for campaign generation."""
        with get_session() as session:
            from sqlmodel import select
            stmt = select(IntelStory).where(IntelStory.id == story_id)
            story = session.exec(stmt).first()
            if not story:
                return None
            return {
                "title": story.title,
                "url": story.url,
                "content": story.full_content,
                "source": story.source,
            }
