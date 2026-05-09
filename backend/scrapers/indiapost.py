import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

from bs4 import BeautifulSoup
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

logger = logging.getLogger(__name__)

SCRAPE_URLS = [
    "https://www.indiapost.gov.in/VAS/Pages/Whatsnew.aspx",
    "https://www.indiapost.gov.in/VAS/Pages/pressRelease.aspx",
]


class IndiaPostScraper(BaseScraper):
    def scrape(self) -> List[Dict[str, Any]]:
        items = self._scrape_site()
        if not items:
            items = self._fallback()
        return items

    def _scrape_site(self) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []

        for page_url in SCRAPE_URLS:
            resp = self.fetch_url(page_url)
            if not resp:
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            # India Post uses SharePoint / table layouts
            for link in soup.select(
                "table a, .ms-rtestate-field a, ul.news-list li a, "
                ".ms-WPBody a, .s4-wpcell a"
            )[:20]:
                title = link.get_text(strip=True)
                href = link.get("href", "")

                if not title or len(title) < 10:
                    continue
                if not href.startswith("http"):
                    href = "https://www.indiapost.gov.in" + href

                items.append(
                    {
                        "category": "indiapost",
                        "title": title,
                        "summary": "Official update from India Post (indiapost.gov.in).",
                        "source": "India Post",
                        "url": href,
                        "published_at": datetime.now(timezone.utc),
                        "alert_level": "none",
                    }
                )

        return items

    def _fallback(self) -> List[Dict[str, Any]]:
        logger.warning("indiapost.gov.in scrape failed; using Google News fallback")
        return parse_rss_feed(
            "https://news.google.com/rss/search?q=india+post+postal+department"
            "+when:7d&hl=en-IN&gl=IN&ceid=IN:en",
            "India Post (via Google News)",
            "indiapost",
            max_items=8,
        )
