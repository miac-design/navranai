"""
Phase 20: Scheduled Auto-Publish Pipeline.

Uses APScheduler to create timed publishing jobs for approved campaigns.
Can trigger download-ready ZIP bundles or future direct API publishing.
"""
import os
import logging
import zipfile
import json
from datetime import datetime, timedelta
from typing import Optional
from src.models import Campaign, Post, get_session

logger = logging.getLogger("redm.scheduler")

# APScheduler is optional
try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.date import DateTrigger
    SCHEDULER_AVAILABLE = True
except ImportError:
    SCHEDULER_AVAILABLE = False
    logger.warning("APScheduler not installed — scheduling disabled")


# Default publish times per day of week
DEFAULT_PUBLISH_TIMES = {
    0: "09:00",  # Monday 9 AM
    1: "09:00",  # Tuesday
    2: "12:00",  # Wednesday noon
    3: "09:00",  # Thursday
    4: "15:00",  # Friday 3 PM (Hope post)
}


class PublishScheduler:
    """Manages scheduled publishing of approved campaigns."""

    def __init__(self):
        self.scheduler = None
        if SCHEDULER_AVAILABLE:
            self.scheduler = AsyncIOScheduler()
            self.scheduler.start()
            logger.info("Publish scheduler started")

    def schedule_campaign(self, campaign_id: str, start_date: Optional[datetime] = None):
        """Create 5 scheduled publish jobs for each post in the campaign."""
        if not self.scheduler:
            logger.warning("Scheduler unavailable")
            return

        if start_date is None:
            # Default to next Monday
            now = datetime.now()
            days_ahead = 7 - now.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            start_date = now.replace(hour=0, minute=0, second=0) + timedelta(days=days_ahead)

        with get_session() as session:
            from sqlmodel import select
            posts = session.exec(
                select(Post).where(Post.campaign_id == campaign_id).order_by(Post.day_of_week)  # type: ignore
            ).all()

            for post in posts:
                day_offset = post.day_of_week
                time_str = DEFAULT_PUBLISH_TIMES.get(day_offset, "09:00")
                hour, minute = map(int, time_str.split(":"))
                publish_dt = start_date + timedelta(days=day_offset)
                publish_dt = publish_dt.replace(hour=hour, minute=minute)

                self.scheduler.add_job(
                    self._execute_publish,
                    trigger=DateTrigger(run_date=publish_dt),
                    args=[post.id],
                    id=f"publish_{campaign_id}_{post.id}",
                    replace_existing=True,
                )
                logger.info("Scheduled %s post for %s", post.content_type, publish_dt.isoformat())

    async def _execute_publish(self, post_id: str):
        """Execute a scheduled publish — creates a download bundle."""
        logger.info("PUBLISHING post %s", post_id)
        # In a real system, this would call social media APIs.
        # For now, we mark the post as published.
        with get_session() as session:
            from sqlmodel import select
            post = session.exec(select(Post).where(Post.id == post_id)).first()
            if post:
                post.status = "published"
                session.add(post)
                session.commit()
                logger.info("Published %s post: %s", post.content_type, post.caption[:50])

    def create_download_bundle(self, campaign_id: str) -> Optional[str]:
        """Create a ZIP file with all campaign assets for manual download."""
        output_dir = os.getenv("OUTPUT_DIR", "outputs")
        zip_path = os.path.join(output_dir, f"campaign_{campaign_id}.zip")

        try:
            with get_session() as session:
                from sqlmodel import select
                posts = session.exec(
                    select(Post).where(Post.campaign_id == campaign_id)
                ).all()

                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    manifest = []
                    for post in posts:
                        day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][post.day_of_week]
                        content_type = post.content_type

                        # Add caption
                        caption_name = f"{day_name}_{content_type}_caption.txt"
                        caption_content = (
                            f"Content Type: {content_type.upper()}\n"
                            f"Day: {day_name}\n"
                            f"Hashtags: {post.hashtags}\n\n"
                            f"{post.caption}"
                        )
                        zf.writestr(caption_name, caption_content)

                        # Add images
                        renders = json.loads(post.platform_renders) if post.platform_renders else {}
                        for platform, img_url in renders.items():
                            local_img = img_url.replace("http://localhost:8000/", "")
                            if os.path.exists(local_img):
                                zf.write(local_img, f"{day_name}_{content_type}_{platform}.png")

                        manifest.append({
                            "day": day_name,
                            "type": content_type,
                            "caption_file": caption_name,
                            "platforms": list(renders.keys()),
                        })

                    zf.writestr("manifest.json", json.dumps(manifest, indent=2))

            logger.info("Created download bundle: %s", zip_path)
            return zip_path

        except Exception as e:
            logger.error("Bundle creation failed: %s", e)
            return None

    def get_scheduled_jobs(self) -> list[dict]:
        """Get all pending scheduled publish jobs."""
        if not self.scheduler:
            return []

        jobs = self.scheduler.get_jobs()
        return [
            {
                "id": job.id,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else "",
                "args": str(job.args),
            }
            for job in jobs
        ]
