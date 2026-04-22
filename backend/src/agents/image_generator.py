"""
Phase 4: Content-Type-Aware Image Generator.

Two-phase generation:
  Phase 1 — Gemini generates a text-free cinematic photograph (per content type).
  Phase 2 — Pillow composites headline/facts/source onto the image.
"""
import os
import logging
from datetime import datetime
from google import genai
from google.genai import types
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langsmith import traceable
from pydantic import BaseModel, Field
from PIL import Image, ImageDraw, ImageFont
from src.state import AgentState, CampaignPost

logger = logging.getLogger("redm.image_gen")


# ---------------------------------------------------------------------------
# Per-type visual treatments (Phase 4)
# ---------------------------------------------------------------------------
TYPE_VISUAL_OVERRIDES = {
    "reactive": "Dark cinematic tones, urgency, news-photography feel. Deep shadows, desaturated, editorial gravity.",
    "stat": "Clean, light background. Minimal photography. High contrast for number overlay. Almost infographic-like simplicity.",
    "explainer": "Blue educational tone. Soft gradients, light backgrounds, calm and approachable. Infographic-adjacent feel.",
    "action": "Dark + bold. High contrast. Space for red CTA overlay. Urgent but empowering. Like a movie poster.",
    "hope": "Warm sunrise tones. Golden hour photography. Soft amber gradients. Uplifting, peaceful, forward-looking.",
}


class OverlayText(BaseModel):
    headline: str = Field(description="Event headline, max 8 words.")
    key_fact: str = Field(description="One specific data point. NEVER invent numbers.")
    source_line: str = Field(description="Short attribution, e.g. 'Source: Reuters'.")


# Font loading
_FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "config", "fonts")

def _load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = os.path.normpath(os.path.join(_FONT_DIR, name))
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        for fb in ["arial.ttf", "arialbd.ttf"]:
            try:
                return ImageFont.truetype(fb, size)
            except (OSError, IOError):
                continue
        return ImageFont.load_default()


class ImageGeneratorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        self.text_extractor = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(OverlayText)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY is not set")
        self.genai_client = genai.Client(api_key=api_key)
        self._visual_philosophy = self._load_file("visual_philosophy.md")

    @staticmethod
    def _load_file(name: str) -> str:
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "config", name))
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    @traceable(name="Image Generation")
    def generate_image(self, state: AgentState) -> dict:
        """Generate an image for the current post in the campaign."""
        posts = state.get("campaign_posts", [])
        idx = state.get("current_post_index", 0)

        if not posts or idx >= len(posts):
            return {"status": "error", "feedback": "No post to generate image for."}

        post = CampaignPost(**posts[idx])
        content_type = post.content_type
        logger.info("--- IMAGE GEN: Creating %s image (index %d) ---", content_type, idx)

        caption = post.caption
        if not caption:
            return {"status": "error", "feedback": "No caption available for image generation."}

        # Phase 4: Get type-specific visual override
        visual_override = TYPE_VISUAL_OVERRIDES.get(content_type, "")
        visual_style = state.get("visual_style", "") + " " + visual_override
        visual_elements = post.visual_suggestion or state.get("visual_elements", "")
        topic = state.get("trend_topic", "")
        context = state.get("trend_context", "")
        user_guidance = state.get("user_guidance", "")

        # Build image prompt
        prompt_template = ChatPromptTemplate.from_template("""
You are a minimalist photography director for an anti-trafficking awareness campaign.

DESIGN PHILOSOPHY:
{visual_philosophy}

CONTENT TYPE: {content_type}
TYPE-SPECIFIC DIRECTION: {visual_override}

EVENT:
Headline: {topic}
Context: {context}

VISUAL STYLE: {visual_style}
VISUAL ANCHOR: {visual_elements}
{user_guidance_block}

RULES:
1. ONE subject only. No multiple symbols.
2. 50-60% negative space.
3. Shallow depth of field.
4. 2-3 color tones max.
5. Bottom 25% dark for text overlay.
6. No text/captions in the image.

SAFETY:
- Anonymous figures only (silhouettes, backs, hands).
- No children, violence, sexual content.

OUTPUT: One paragraph under 120 words. Pure photography, no text.
""")

        user_guidance_block = f"USER DIRECTION:\n{user_guidance}" if user_guidance else ""
        chain = prompt_template | self.llm
        image_prompt = chain.invoke({
            "visual_philosophy": self._visual_philosophy,
            "content_type": content_type.upper(),
            "visual_override": visual_override,
            "topic": topic,
            "context": context,
            "visual_style": visual_style,
            "visual_elements": visual_elements,
            "user_guidance_block": user_guidance_block,
        }).content

        # Handle image feedback for regeneration
        feedback = state.get("image_feedback")
        if feedback:
            image_prompt += f"\nCRITICAL REGENERATION INSTRUCTION: {feedback}"

        # Extract overlay text
        overlay: OverlayText = self.text_extractor.invoke([
            SystemMessage(content="Extract headline (max 8 words), key fact, and source from the post. NEVER invent statistics."),
            HumanMessage(content=f"Headline: {topic}\nContext: {context}\nPost: {caption}"),
        ])
        overlay_text = {"headline": overlay.headline, "key_fact": overlay.key_fact, "source_line": overlay.source_line}

        # Generate via Gemini
        logger.info("Calling Gemini API for image generation...")
        try:
            image_part, block_reason = self._call_gemini(image_prompt)

            if image_part is None and "SAFETY" in (block_reason or "").upper():
                logger.info("Safety-blocked — retrying with softened prompt")
                image_prompt = self._soften_prompt(image_prompt, topic)
                image_part, block_reason = self._call_gemini(image_prompt)

            if image_part is None:
                logger.error("Gemini returned no image: %s", block_reason)
                return {"status": "error", "feedback": f"Image blocked: {block_reason}"}

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = os.getenv("OUTPUT_DIR", "outputs")
            os.makedirs(output_dir, exist_ok=True)

            raw_path = os.path.join(output_dir, f"raw_{content_type}_{timestamp}.png")
            with open(raw_path, "wb") as f:
                f.write(image_part.inline_data.data)

            final_path = os.path.join(output_dir, f"{content_type}_{timestamp}.png")
            self._composite_text_overlay(raw_path, final_path, overlay_text, visual_style)

            image_url = f"http://localhost:8000/{final_path.replace(os.sep, '/')}"

            post.image_path = image_url
            post.image_prompt = image_prompt
            posts[idx] = post.model_dump()

            logger.info("Image saved: %s", final_path)
            return {"campaign_posts": posts, "status": "generating_image"}

        except Exception as e:
            logger.error("Image generation failed: %s", e)
            return {"status": "error", "feedback": str(e)}

    def _call_gemini(self, prompt: str):
        try:
            result = self.genai_client.models.generate_content(
                model="gemini-3.1-flash-image-preview",
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="4:5", image_size="1K"),
                ),
            )
            if result.candidates and result.candidates[0].content and result.candidates[0].content.parts:
                return result.candidates[0].content.parts[0], None
            reason = "Unknown"
            if hasattr(result, "prompt_feedback") and result.prompt_feedback:
                reason = str(result.prompt_feedback)
            return None, reason
        except Exception as e:
            return None, str(e)

    def _soften_prompt(self, original: str, topic: str) -> str:
        softener = ChatPromptTemplate.from_template("""
Rewrite this blocked image prompt as a symbolic, abstract photograph that passes moderation.

ORIGINAL: {original_prompt}
TOPIC: {topic}

RULES:
1. Replace distress scenes with ONE symbolic object (open door, broken chain, empty chair).
2. ONE subject, 50-60% negative space, 2-3 tones. Minimalist.
3. No people in distress. No text. Bottom 25% dark.
4. Under 100 words.
""")
        return (softener | self.llm).invoke({"original_prompt": original, "topic": topic}).content

    def _composite_text_overlay(self, bg_path: str, out_path: str, overlay: dict, visual_style: str = ""):
        img = Image.open(bg_path).convert("RGBA")
        w, h = img.size
        accent = self._pick_accent(visual_style)

        hl_size = max(int(h * 0.055), 28)
        fact_size = max(int(h * 0.035), 18)
        src_size = max(int(h * 0.022), 13)

        font_hl = _load_font("PlayfairDisplay[wght].ttf", hl_size)
        font_fact = _load_font("Roboto[wdth,wght].ttf", fact_size)
        font_src = _load_font("Roboto[wdth,wght].ttf", src_size)

        ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(ov)

        # Bottom gradient
        gs = int(h * 0.55)
        for y in range(gs, h):
            p = (y - gs) / (h - gs)
            a = int(210 * (p ** 1.5))
            draw.rectangle([(0, y), (w, y + 1)], fill=(0, 0, 0, a))

        margin = int(w * 0.06)
        max_tw = w - 2 * margin
        sp = int(h * 0.015)

        src_text = overlay.get("source_line", "")
        src_y = h - int(h * 0.035)
        draw.text((margin, src_y), src_text, font=font_src, fill=(200, 200, 200, 220))

        kf = overlay.get("key_fact", "")
        kf_lines = self._wrap(kf, font_fact, max_tw, draw)
        kf_h = len(kf_lines) * (fact_size + 4)
        kf_y = src_y - kf_h - sp
        self._draw_shadow_text(draw, kf, font_fact, accent, (0, 0, 0, 200), margin, kf_y, max_tw)

        hl = overlay.get("headline", "").upper()
        hl_lines = self._wrap(hl, font_hl, max_tw, draw)
        hl_h = len(hl_lines) * (hl_size + 4)
        hl_y = kf_y - hl_h - sp
        self._draw_shadow_text(draw, hl, font_hl, (255, 255, 255), (0, 0, 0, 200), margin, hl_y, max_tw)

        bar_h = max(int(h * 0.005), 3)
        bar_y = hl_y - int(h * 0.015) - bar_h
        draw.rectangle([(margin, bar_y), (w - margin, bar_y + bar_h)], fill=accent)

        composite = Image.alpha_composite(img, ov).convert("RGB")
        composite.save(out_path, quality=95)

    def _draw_shadow_text(self, draw, text, font, color, shadow, x, y, max_w):
        for i, line in enumerate(self._wrap(text, font, max_w, draw)):
            ly = y + i * (font.size + 4)
            draw.text((x + 2, ly + 2), line, font=font, fill=shadow)
            draw.text((x, ly), line, font=font, fill=color)

    @staticmethod
    def _wrap(text, font, max_w, draw):
        words, lines, cur = text.split(), [], ""
        for w in words:
            test = f"{cur} {w}".strip()
            bb = draw.textbbox((0, 0), test, font=font)
            if bb[2] - bb[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines or [""]

    @staticmethod
    def _pick_accent(style: str) -> tuple:
        s = style.lower()
        if "neon" in s or "vibrant" in s:
            return (0, 255, 170, 255)
        elif "corporate" in s or "blue-steel" in s:
            return (100, 180, 255, 255)
        elif "warm" in s and "amber" in s:
            return (255, 200, 80, 255)
        elif "hope" in s or "sunrise" in s or "golden" in s:
            return (255, 180, 60, 255)
        elif "action" in s or "bold" in s:
            return (173, 31, 36, 255)
        elif "blue" in s or "educational" in s:
            return (59, 130, 246, 255)
        else:
            return (255, 200, 0, 255)
