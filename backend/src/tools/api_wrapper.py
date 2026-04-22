"""
Reliability wrapper for news API tools.
Features: retries with exponential backoff, fallback content extraction via Crawl4AI.
"""
import functools
import time
import logging
from src.tools.crawl4ai_scraper import Crawl4AIScraper

logger = logging.getLogger("redm.api_wrapper")


def reliable_news_tool(max_retries=3, timeout_seconds=30):
    """Decorator that adds retry logic and content-extraction fallbacks to news tools."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    results = func(*args, **kwargs)
                    standardized = []
                    scraper = Crawl4AIScraper()

                    for item in results:
                        title = item.get("title", "Unknown Title")
                        source = item.get("source", "Unknown Source")
                        url = item.get("url", "")
                        content = item.get("content", "")
                        timestamp = item.get("timestamp", "")

                        # Fallback: if URL exists but content is thin, scrape it
                        if url and (not content or len(content.strip()) < 50):
                            logger.info("Extracting full text via Crawl4AI for %s", url)
                            extracted = scraper.read_url(url)
                            if extracted:
                                content = extracted

                        standardized.append({
                            "title": title,
                            "source": source,
                            "url": url,
                            "content": content,
                            "timestamp": timestamp,
                        })
                    return standardized

                except Exception as e:
                    last_exception = e
                    logger.warning("Attempt %d/%d failed for %s: %s", attempt + 1, max_retries, func.__name__, e)
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)

            logger.error("All %d attempts failed for %s", max_retries, func.__name__)
            return []
        return wrapper
    return decorator
