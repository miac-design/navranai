"""
Publisher Agent — Formats and packages final approved content.
Migrated from V2, updated for multi-post campaigns.
"""
import os
import json
import logging
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState

logger = logging.getLogger("redm.publisher")


class PublisherAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    def format_for_platforms(self, caption: str, content_type: str) -> dict:
        """Format a caption for multiple platforms."""
        prompt = ChatPromptTemplate.from_template("""
Format this social media post for both X (Twitter) and Instagram.

STRUCTURE:
1. X (max 280 characters, punchy)
2. Instagram (longer, more descriptive)

Content Type: {content_type}

Original: {caption}

Return JSON with keys "x" and "instagram".
""")
        chain = prompt | self.llm
        result = chain.invoke({"caption": caption, "content_type": content_type}).content

        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"x": caption[:280], "instagram": caption}

    def create_preview_html(self, campaign_posts: list, output_dir: str = "outputs") -> str:
        """Generate an HTML preview of all campaign posts."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"campaign_preview_{timestamp}.html"
        path = os.path.join(output_dir, filename)
        os.makedirs(output_dir, exist_ok=True)

        cards_html = ""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        type_colors = {
            "reactive": "#EF4444", "stat": "#3B82F6", "explainer": "#8B5CF6",
            "action": "#F59E0B", "hope": "#10B981",
        }

        for post in campaign_posts:
            ct = post.get("content_type", "reactive")
            day = days[post.get("day_of_week", 0)]
            color = type_colors.get(ct, "#6B7280")
            caption = post.get("caption", "").replace("\n", "<br>")
            img = post.get("image_path", "")

            cards_html += f"""
            <div class="card">
                <div class="card-header" style="background:{color}">{day} — {ct.upper()}</div>
                <div class="card-body">
                    <p>{caption}</p>
                    {"<img src='" + img + "' class='card-img'>" if img else ""}
                </div>
            </div>"""

        html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Campaign Preview</title>
<style>
body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; margin: 0; padding: 20px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; max-width: 1200px; margin: auto; }}
.card {{ background: #16213e; border-radius: 12px; overflow: hidden; }}
.card-header {{ padding: 12px 16px; color: white; font-weight: bold; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }}
.card-body {{ padding: 16px; font-size: 14px; line-height: 1.6; }}
.card-img {{ width: 100%; border-radius: 8px; margin-top: 12px; }}
h1 {{ text-align: center; color: #AD1F24; margin-bottom: 30px; }}
</style></head>
<body><h1>🔴 RedM Campaign Preview</h1><div class="grid">{cards_html}</div></body></html>"""

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

        logger.info("Preview saved: %s", path)
        return path
