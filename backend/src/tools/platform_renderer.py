"""
Phase 5: Multi-Platform Renderer.

Takes a master image and produces platform-specific sizes:
  IG Square (1080x1080), IG Stories (1080x1920), X Card (1600x900),
  LinkedIn (1200x627), Facebook (1200x630).
"""
import os
import logging
from PIL import Image, ImageOps
from src.state import AgentState, CampaignPost
from config import PLATFORM_SPECS

logger = logging.getLogger("redm.renderer")


class PlatformRenderer:
    """Resizes a master image to multiple platform-specific dimensions."""

    def render_platforms(self, state: AgentState) -> dict:
        """Render current post's image into all platform sizes."""
        posts = state.get("campaign_posts", [])
        idx = state.get("current_post_index", 0)

        if not posts or idx >= len(posts):
            return {"status": "error", "feedback": "No post to render."}

        post = CampaignPost(**posts[idx])
        image_path = post.image_path

        if not image_path:
            logger.warning("No image path for post %d — skipping render", idx)
            return {"campaign_posts": posts, "status": "rendering"}

        # Resolve the path (strip URL prefix if present)
        local_path = image_path
        if local_path.startswith("http://localhost:8000/"):
            local_path = local_path.replace("http://localhost:8000/", "")

        if not os.path.exists(local_path):
            logger.warning("Image file not found: %s", local_path)
            return {"campaign_posts": posts, "status": "rendering"}

        logger.info("--- RENDERER: Creating platform sizes for %s ---", post.content_type)

        try:
            master = Image.open(local_path)
            output_dir = os.path.dirname(local_path)
            base_name = os.path.splitext(os.path.basename(local_path))[0]

            renders = {}
            for platform, (target_w, target_h) in PLATFORM_SPECS.items():
                resized = self._smart_resize(master.copy(), target_w, target_h)
                render_path = os.path.join(output_dir, f"{base_name}_{platform}.png")
                resized.save(render_path, quality=95)
                render_url = f"http://localhost:8000/{render_path.replace(os.sep, '/')}"
                renders[platform] = render_url
                logger.info("  → %s: %dx%d saved", platform, target_w, target_h)

            post.platform_renders = renders
            posts[idx] = post.model_dump()

            return {"campaign_posts": posts, "status": "rendering"}

        except Exception as e:
            logger.error("Platform rendering failed: %s", e)
            return {"campaign_posts": posts, "status": "rendering"}

    @staticmethod
    def _smart_resize(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
        """
        Resize with smart cropping that protects the bottom 25% of the image
        (where text overlays live).
        """
        src_w, src_h = img.size
        target_ratio = target_w / target_h
        src_ratio = src_w / src_h

        if abs(src_ratio - target_ratio) < 0.05:
            # Nearly same aspect ratio — simple resize
            return img.resize((target_w, target_h), Image.LANCZOS)

        if target_ratio > src_ratio:
            # Target is wider — crop top (protect bottom text zone)
            new_h = int(src_w / target_ratio)
            # Crop from top, keeping bottom
            top = max(0, src_h - new_h)
            img = img.crop((0, top, src_w, src_h))
        else:
            # Target is taller — center horizontally
            new_w = int(src_h * target_ratio)
            left = max(0, (src_w - new_w) // 2)
            img = img.crop((left, 0, left + new_w, src_h))

        return img.resize((target_w, target_h), Image.LANCZOS)
