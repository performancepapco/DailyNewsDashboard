from typing import List, Dict, Any
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

RSS_SOURCES = [
    ("https://www.thehindu.com/news/national/andhra-pradesh/?service=rss", "The Hindu AP"),
    ("https://www.newindianexpress.com/states/andhra-pradesh/feed", "New Indian Express AP"),
    (
        "https://news.google.com/rss/search?q=Andhra+Pradesh+news+when:24h"
        "&hl=en-IN&gl=IN&ceid=IN:en",
        "Andhra Pradesh News",
    ),
    (
        "https://news.google.com/rss/search?q=Amaravati+OR+Vijayawada+OR+YSRCP+OR+TDP"
        "+when:24h&hl=en-IN&gl=IN&ceid=IN:en",
        "AP Politics & Development",
    ),
]


class AndhraScraper(BaseScraper):
    def scrape(self) -> List[Dict[str, Any]]:
        all_items: List[Dict[str, Any]] = []
        for url, source in RSS_SOURCES:
            all_items.extend(parse_rss_feed(url, source, "andhra", max_items=8))
        return all_items
