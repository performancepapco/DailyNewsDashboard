from typing import List, Dict, Any
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

RSS_SOURCES = [
    (
        "https://news.google.com/rss/search?q=viral+trending+story+week&hl=en&gl=US&ceid=US:en",
        "Google News Viral",
    ),
    (
        "https://news.google.com/rss/search?q=viral+news+trending+india&hl=en&gl=IN&ceid=IN:en",
        "Google News Trending India",
    ),
    ("https://mashable.com/feeds/rss/all", "Mashable"),
    ("https://time.com/feed/", "TIME"),
    ("https://www.reddit.com/r/worldnews.rss", "Reddit World News"),
]

_VIRAL_TERMS = {
    "viral", "trending", "most read", "popular", "sensation", "goes viral",
    "breaking", "shocking", "incredible", "world record", "bizarre",
    "extraordinary", "unprecedented", "surprising", "remarkable", "stunning",
}


class ViralNewsScraper(BaseScraper):
    def scrape(self) -> List[Dict[str, Any]]:
        all_items: List[Dict[str, Any]] = []
        for url, source in RSS_SOURCES:
            raw = parse_rss_feed(url, source, "viral_news", max_items=12)
            for item in raw:
                item["category"] = "viral_news"
            all_items.extend(raw)
        return all_items
