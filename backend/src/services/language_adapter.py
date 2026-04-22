"""
Phase 18: Multi-Language Adapter.

Translates approved captions into target languages using GPT-4o-mini.
Supports: English, Spanish, French, Portuguese.
"""
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from langsmith import traceable
from config import SUPPORTED_LANGUAGES

logger = logging.getLogger("redm.language")


LANGUAGE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "pt": "Portuguese",
}


class TranslatedPost(BaseModel):
    caption: str = Field(description="The translated caption")
    hashtags: list[str] = Field(description="Translated/localized hashtags")
    cultural_notes: str = Field(default="", description="Any cultural adaptation notes")


class LanguageAdapter:
    """Translates campaign content into supported languages."""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2).with_structured_output(TranslatedPost)

    @traceable(name="Language Translation")
    def translate(self, caption: str, hashtags: list[str], target_lang: str) -> dict:
        """Translate a post to the target language with cultural adaptation."""
        if target_lang not in SUPPORTED_LANGUAGES:
            logger.warning("Unsupported language: %s", target_lang)
            return {"caption": caption, "hashtags": hashtags, "cultural_notes": ""}

        if target_lang == "en":
            return {"caption": caption, "hashtags": hashtags, "cultural_notes": "Original language"}

        lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
        logger.info("Translating to %s", lang_name)

        result: TranslatedPost = self.llm.invoke([
            SystemMessage(content=(
                f"You are a professional translator for a human trafficking awareness campaign.\n"
                f"Translate the following social media post into {lang_name}.\n\n"
                f"RULES:\n"
                f"1. Preserve the emotional tone and urgency.\n"
                f"2. Adapt hashtags to the target language (use popular local equivalents).\n"
                f"3. Localize the hotline number if a regional equivalent exists, otherwise keep 1-888-373-7888.\n"
                f"4. Use the same ethical language principles in the target language.\n"
                f"5. Note any cultural adaptations you made."
            )),
            HumanMessage(content=(
                f"ORIGINAL POST:\n{caption}\n\n"
                f"HASHTAGS: {', '.join(hashtags)}\n\n"
                f"Translate to {lang_name}."
            )),
        ])

        return {
            "caption": result.caption,
            "hashtags": result.hashtags,
            "cultural_notes": result.cultural_notes,
        }

    def translate_campaign(self, posts: list[dict], target_lang: str) -> list[dict]:
        """Translate all posts in a campaign."""
        translated = []
        for post in posts:
            try:
                result = self.translate(
                    post.get("caption", ""),
                    post.get("hashtags", []),
                    target_lang,
                )
                translated_post = post.copy()
                translated_post["caption"] = result["caption"]
                translated_post["hashtags"] = result["hashtags"]
                translated.append(translated_post)
            except Exception as e:
                logger.error("Translation failed for post: %s", e)
                translated.append(post)
        return translated
