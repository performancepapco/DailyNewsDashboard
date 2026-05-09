import logging
import random
import time
from datetime import datetime, timezone
from typing import List, Dict, Any

from .base import BaseScraper
from .rss_scraper import parse_rss_feed

logger = logging.getLogger(__name__)


class GoogleTrendsScraper(BaseScraper):
    def scrape(self) -> List[Dict[str, Any]]:
        try:
            from pytrends.request import TrendReq

            time.sleep(random.uniform(3, 7))   # rate-limit courtesy delay
            pt = TrendReq(hl="en-IN", tz=330, timeout=(10, 25))
            trending = pt.trending_searches(pn="india")

            items: List[Dict[str, Any]] = []
            for _, row in trending.head(10).iterrows():
                topic = str(row.iloc[0]).strip()
                if not topic:
                    continue
                search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}&tbm=nws"
                items.append(
                    {
                        "category": "google_trends",
                        "title": f"Trending: {topic}",
                        "summary": f'"{topic}" is currently one of the top trending searches on Google in India.',
                        "source": "Google Trends India",
                        "url": search_url,
                        "published_at": datetime.now(timezone.utc),
                        "alert_level": "none",
                    }
                )
            return items

        except Exception as exc:
            logger.warning(f"pytrends failed ({exc}); using Google News top stories as fallback")
            return self._fallback()

    def _fallback(self) -> List[Dict[str, Any]]:
        return parse_rss_feed(
            "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en",
            "Google News India Top Stories",
            "google_trends",
            max_items=5,
        )
