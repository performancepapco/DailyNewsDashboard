import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

from bs4 import BeautifulSoup
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

logger = logging.getLogger(__name__)

_KEYWORDS = {
    "dopt", "india post", "department of posts", "postal", "ccs rules",
    "service rules", "recruitment", "promotion", "cadre", "deputation",
    "pension", "leave rules", "administrative",
}


class GazetteScraper(BaseScraper):
    def scrape(self) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []

        # Primary: Google News for recent gazette notifications
        items.extend(
            parse_rss_feed(
                "https://news.google.com/rss/search?q=gazette+notification+india+post"
                "+OR+DoPT+OR+%22department+of+posts%22+when:7d"
                "&hl=en-IN&gl=IN&ceid=IN:en",
                "Gazette Notification",
                "gazette",
                max_items=10,
            )
        )

        # Secondary: egazette.nic.in homepage scrape
        resp = self.fetch_url("https://egazette.nic.in/")
        if resp:
            soup = BeautifulSoup(resp.text, "html.parser")
            for link in soup.select("a")[:60]:
                title = link.get_text(strip=True)
                href = link.get("href", "")

                if len(title) < 15:
                    continue
                if not any(kw in title.lower() for kw in _KEYWORDS):
                    continue

                if href and not href.startswith("http"):
                    href = "https://egazette.nic.in/" + href.lstrip("/")

                items.append(
                    {
                        "category": "gazette",
                        "title": title,
                        "summary": "Official Government of India gazette notification.",
                        "source": "eGazette India",
                        "url": href,
                        "published_at": datetime.now(timezone.utc),
                        "alert_level": "important",
                    }
                )

        return items
