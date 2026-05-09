import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

from bs4 import BeautifulSoup
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

logger = logging.getLogger(__name__)
BASE_URL = "https://www.gconnect.in"


class GConnectScraper(BaseScraper):
    def scrape(self) -> List[Dict[str, Any]]:
        items = self._scrape_site()
        if not items:
            items = self._fallback()
        return items

    def _scrape_site(self) -> List[Dict[str, Any]]:
        resp = self.fetch_url(BASE_URL + "/")
        if not resp:
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        items: List[Dict[str, Any]] = []

        # WordPress standard selectors; GConnect is a WP blog
        for article in soup.select("article, .post, .entry")[:20]:
            title_el = article.select_one("h2 a, h3 a, .entry-title a, h1 a")
            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            href = title_el.get("href", "")
            if not href.startswith("http"):
                href = BASE_URL + href

            summary_el = article.select_one(".entry-summary p, .excerpt, p")
            summary = summary_el.get_text(strip=True)[:400] if summary_el else ""

            published_at = datetime.now(timezone.utc)
            date_el = article.select_one("time[datetime], .entry-date, .published")
            if date_el:
                try:
                    dt_str = date_el.get("datetime") or date_el.get_text(strip=True)
                    published_at = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
                except Exception:
                    pass

            if title and len(title) > 10:
                items.append(
                    {
                        "category": "gconnect",
                        "title": title,
                        "summary": summary,
                        "source": "GConnect",
                        "url": href,
                        "published_at": published_at,
                        "alert_level": "none",
                    }
                )

        return items

    def _fallback(self) -> List[Dict[str, Any]]:
        logger.warning("GConnect direct scrape failed; falling back to Google News")
        return parse_rss_feed(
            "https://news.google.com/rss/search?q=central+government+employees"
            "+7th+pay+DA+pension+when:7d&hl=en-IN&gl=IN&ceid=IN:en",
            "GConnect (via Google News)",
            "gconnect",
            max_items=8,
        )
