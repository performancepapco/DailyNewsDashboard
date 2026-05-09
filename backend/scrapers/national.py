from typing import List, Dict, Any
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

RSS_SOURCES = [
    ("https://www.thehindu.com/news/national/?service=rss", "The Hindu"),
    ("https://indianexpress.com/section/india/feed/", "Indian Express"),
    ("https://economictimes.indiatimes.com/news/india/rssfeeds/1022159112.cms", "Economic Times"),
    ("https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml", "Hindustan Times"),
    (
        "https://news.google.com/rss/search?q=india+government+policy+parliament"
        "+when:24h&hl=en-IN&gl=IN&ceid=IN:en",
        "India Governance",
    ),
]


class NationalScraper(BaseScraper):
    def scrape(self) -> List[Dict[str, Any]]:
        all_items: List[Dict[str, Any]] = []
        for url, source in RSS_SOURCES:
            all_items.extend(parse_rss_feed(url, source, "national", max_items=8))
        return all_items
