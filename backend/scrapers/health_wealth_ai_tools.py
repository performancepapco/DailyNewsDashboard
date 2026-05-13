from typing import List, Dict, Any
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

# Domain-specific sources need no keyword filtering — the source/query already targets the topic
ALL_SOURCES = [
    # Health
    ("https://www.who.int/feeds/entity/mediacentre/news/en/rss.xml", "WHO"),
    (
        "https://news.google.com/rss/search?q=health+wellness+medical+tips+india&hl=en&gl=IN&ceid=IN:en",
        "Health News",
    ),
    ("https://www.healthline.com/rss/health-news", "Healthline"),
    # Wealth & Finance
    (
        "https://news.google.com/rss/search?q=investment+savings+personal+finance+india&hl=en&gl=IN&ceid=IN:en",
        "Finance News India",
    ),
    ("https://www.moneycontrol.com/rss/latestnews.xml", "Moneycontrol"),
    (
        "https://economictimes.indiatimes.com/wealth/rssfeeds/44745066.cms",
        "ET Wealth",
    ),
    # AI New Tools
    (
        "https://news.google.com/rss/search?q=new+AI+tool+app+launch+2025&hl=en&gl=US&ceid=US:en",
        "AI Tools News",
    ),
    ("https://venturebeat.com/category/ai/feed/", "VentureBeat AI"),
    ("https://techcrunch.com/tag/artificial-intelligence/feed/", "TechCrunch AI"),
]

# Light filter only for Moneycontrol (broad source) — single words to avoid false negatives
_MONEYCONTROL_TERMS = {
    "investment", "stock", "finance", "money", "market", "fund",
    "tax", "gold", "insurance", "wealth", "returns", "savings",
    "mutual", "portfolio", "equity", "debt", "income",
}


class HealthWealthAIScraper(BaseScraper):
    top_n = 10

    def scrape(self) -> List[Dict[str, Any]]:
        all_items: List[Dict[str, Any]] = []

        for url, source in ALL_SOURCES:
            raw = parse_rss_feed(url, source, "health_wealth_ai", max_items=10)
            if source == "Moneycontrol":
                raw = [
                    item for item in raw
                    if any(
                        kw in item["title"].lower() or kw in item["summary"].lower()
                        for kw in _MONEYCONTROL_TERMS
                    )
                ]
            all_items.extend(raw)

        return all_items
