import logging
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote
from langsmith import traceable

logger = logging.getLogger("redm.gnews")


class GoogleNewsSearch:
    """Fetch human trafficking news via Google News RSS feed."""

    RSS_URL = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en&when=7d"

    # Trusted domains — same as config.py
    TRUSTED_DOMAINS = [
        "reuters.com", "apnews.com", "theguardian.com",
        "bbc.com", "cnn.com", "aljazeera.com",
        "unodc.org", "polarisproject.org", "hrw.org",
        "ijm.org", "ilo.org", "thorn.org",
    ]

    @traceable(name="Google News RSS Search")
    def search_news(self, query: str = '"human trafficking"', num_results: int = 20, restrict_domains: bool = True) -> list:
        """
        Search Google News RSS for articles matching the query.
        If restrict_domains=True, only returns results from trusted domains.
        Only returns articles published within the last 7 days.
        """
        if restrict_domains:
            # Build: "human trafficking" (site:reuters.com OR site:bbc.com OR ...)
            sites = " OR ".join(f"site:{d}" for d in self.TRUSTED_DOMAINS)
            full_query = f'{query} ({sites})'
        else:
            full_query = query

        url = self.RSS_URL.format(query=quote(full_query))
        logger.info("Fetching Google News RSS: %s", url[:120])

        try:
            resp = requests.get(url, timeout=15, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            resp.raise_for_status()
        except Exception as e:
            logger.error("Google News RSS request failed: %s", e)
            return []

        # Parse RSS XML
        try:
            root = ET.fromstring(resp.content)
        except ET.ParseError as e:
            logger.error("Failed to parse RSS XML: %s", e)
            return []

        articles = []
        seen_urls = set()
        cutoff = datetime.now(timezone.utc) - timedelta(days=7)

        for item in root.findall(".//item"):
            if len(articles) >= num_results:
                break

            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            pub_date = item.findtext("pubDate", "").strip()
            source_elem = item.find("source")
            source = source_elem.text.strip() if source_elem is not None and source_elem.text else "Unknown"
            description = item.findtext("description", "").strip()

            # Skip duplicates
            if link in seen_urls:
                continue
            seen_urls.add(link)

            # Filter out articles older than 7 days
            if pub_date:
                try:
                    pub_dt = parsedate_to_datetime(pub_date)
                    if pub_dt < cutoff:
                        logger.debug("Skipping old article (%s): %s", pub_date, title[:60])
                        continue
                except Exception:
                    pass  # If we can't parse the date, keep the article

            # Clean up description (remove HTML tags)
            clean_desc = re.sub(r'<[^>]+>', '', description)

            articles.append({
                "title": title,
                "source": source,
                "url": link,
                "content": clean_desc,
                "timestamp": pub_date,
            })

        logger.info("Google News RSS: %d articles found (7-day filter) for query '%s'", len(articles), query)
        return articles

