from typing import List, Dict, Any
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

RSS_SOURCES = [
    ("https://www.freightwaves.com/feed", "FreightWaves"),
    (
        "https://news.google.com/rss/search?q=india+logistics+freight+supply+chain"
        "+when:24h&hl=en-IN&gl=IN&ceid=IN:en",
        "India Logistics",
    ),
    (
        "https://news.google.com/rss/search?q=shipping+freight+rates+port+container"
        "+when:24h&hl=en&gl=US&ceid=US:en",
        "Global Freight",
    ),
    (
        "https://news.google.com/rss/search?q=e-commerce+warehouse+last+mile+delivery"
        "+when:24h&hl=en-IN&gl=IN&ceid=IN:en",
        "E-Commerce Logistics",
    ),
]


class LogisticsScraper(BaseScraper):
    def scrape(self) -> List[Dict[str, Any]]:
        all_items: List[Dict[str, Any]] = []
        for url, source in RSS_SOURCES:
            all_items.extend(parse_rss_feed(url, source, "logistics", max_items=8))
        return all_items
