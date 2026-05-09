from typing import List, Dict, Any
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

RSS_SOURCES = [
    ("https://feeds.bbci.co.uk/news/world/rss.xml", "BBC World"),
    ("https://www.theguardian.com/world/rss", "The Guardian"),
    ("https://www.aljazeera.com/xml/rss/all.xml", "Al Jazeera"),
    (
        "https://news.google.com/rss/search?q=when:24h+allinurl:reuters.com"
        "&hl=en&gl=US&ceid=US:en",
        "Reuters",
    ),
    (
        "https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com"
        "&hl=en&gl=US&ceid=US:en",
        "AP News",
    ),
]

_EXCLUDE = {"celebrity", "gossip", "fashion", "recipe", "horoscope", "makeup", "style"}


class InternationalScraper(BaseScraper):
    def scrape(self) -> List[Dict[str, Any]]:
        all_items: List[Dict[str, Any]] = []
        for url, source in RSS_SOURCES:
            all_items.extend(parse_rss_feed(url, source, "international", max_items=10))

        return [
            item for item in all_items
            if not any(kw in item["title"].lower() for kw in _EXCLUDE)
        ]
