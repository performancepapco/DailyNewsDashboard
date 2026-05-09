import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

from bs4 import BeautifulSoup
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

logger = logging.getLogger(__name__)


class TwitterTrendsScraper(BaseScraper):
    def scrape(self) -> List[Dict[str, Any]]:
        items = self._scrape_trends24()
        if not items:
            items = self._fallback()
        return items

    def _scrape_trends24(self) -> List[Dict[str, Any]]:
        resp = self.fetch_url("https://trends24.in/india/")
        if not resp:
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        items: List[Dict[str, Any]] = []

        # trends24.in lists trends in ordered list cards
        seen: set = set()
        for el in soup.select(
            ".trend-card__list li a, .trend-list li a, ol li a, .trends-list li a"
        )[:15]:
            topic = el.get_text(strip=True)
            if not topic or topic in seen:
                continue
            seen.add(topic)

            search_url = f"https://x.com/search?q={topic.replace(' ', '%20')}&f=live"
            items.append(
                {
                    "category": "twitter_trends",
                    "title": f"Trending on X: {topic}",
                    "summary": f'"{topic}" is currently trending on X (Twitter) in India.',
                    "source": "X / Twitter Trends India",
                    "url": search_url,
                    "published_at": datetime.now(timezone.utc),
                    "alert_level": "none",
                }
            )

        return items

    def _fallback(self) -> List[Dict[str, Any]]:
        logger.warning("trends24.in unavailable; using Google News India as fallback")
        return parse_rss_feed(
            "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en",
            "India Top Stories (X Fallback)",
            "twitter_trends",
            max_items=5,
        )
