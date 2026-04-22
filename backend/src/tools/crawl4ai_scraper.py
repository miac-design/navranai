"""
Crawl4AI web scraper with requests+BeautifulSoup fallback.
Migrated from V2 with logging cleanup.
"""
import asyncio
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("redm.scraper")


class Crawl4AIScraper:
    async def _crawl_async(self, url: str) -> str:
        from crawl4ai import AsyncWebCrawler
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            return result.markdown

    def read_url(self, url: str) -> str:
        """Read URL content via Crawl4AI, falling back to requests+BeautifulSoup."""
        if not url.startswith("http"):
            url = "https://" + url

        # Attempt 1: Crawl4AI
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            content = loop.run_until_complete(self._crawl_async(url))
            loop.close()
            if content and len(content) > 50:
                return content
        except Exception as e:
            logger.warning("Crawl4AI failed for %s: %s — using fallback", url, e)

        # Attempt 2: requests + BeautifulSoup
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/125.0 Safari/537.36"
            }
            resp = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(resp.text, "html.parser")
            text = " ".join(p.get_text() for p in soup.find_all(["p", "h1", "h2", "h3"]))
            return text
        except Exception as e:
            logger.error("Fallback request also failed for %s: %s", url, e)
            return "ERROR: Could not retrieve article content from the given URL."
