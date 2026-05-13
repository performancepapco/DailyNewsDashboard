from typing import List, Dict, Any
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

# Reliable, credible sources — Google News searches already filter for viral/trending
RSS_SOURCES = [
    (
        "https://news.google.com/rss/search?q=viral+trending+story&hl=en&gl=US&ceid=US:en",
        "Google News Viral",
    ),
    (
        "https://news.google.com/rss/search?q=viral+trending+news+today&hl=en&gl=IN&ceid=IN:en",
        "Google News Trending India",
    ),
    ("https://time.com/feed/", "TIME"),
    ("https://feeds.bbci.co.uk/news/rss.xml", "BBC News"),
    ("https://www.theguardian.com/world/rss", "The Guardian"),
]


class ViralNewsScraper(BaseScraper):
    top_n = 10

    def scrape(self) -> List[Dict[str, Any]]:
        all_items: List[Dict[str, Any]] = []
        for url, source in RSS_SOURCES:
            raw = parse_rss_feed(url, source, "viral_news", max_items=15)
            all_items.extend(raw)
        return all_items
