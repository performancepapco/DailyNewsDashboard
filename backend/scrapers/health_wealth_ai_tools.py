from typing import List, Dict, Any
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

_HEALTH_SOURCES = [
    ("https://www.who.int/feeds/entity/mediacentre/news/en/rss.xml", "WHO"),
    ("https://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC", "WebMD"),
    (
        "https://news.google.com/rss/search?q=health+wellness+medical+breakthrough&hl=en&gl=IN&ceid=IN:en",
        "Health News",
    ),
]

_WEALTH_SOURCES = [
    (
        "https://news.google.com/rss/search?q=personal+finance+wealth+investment+savings+tips&hl=en&gl=IN&ceid=IN:en",
        "Wealth & Finance",
    ),
    ("https://www.moneycontrol.com/rss/latestnews.xml", "Moneycontrol"),
]

_AI_TOOLS_SOURCES = [
    (
        "https://news.google.com/rss/search?q=new+AI+tool+launched+app+release&hl=en&gl=US&ceid=US:en",
        "AI Tools News",
    ),
    ("https://venturebeat.com/category/ai/feed/", "VentureBeat AI"),
]

_HEALTH_TERMS = {
    "health", "wellness", "fitness", "medical", "diet", "mental health",
    "exercise", "nutrition", "vitamin", "disease", "cancer", "diabetes",
    "heart", "weight", "sleep", "stress", "immune", "medicine", "study",
}

_WEALTH_TERMS = {
    "wealth", "investment", "savings", "finance", "stock", "mutual fund",
    "crypto", "gold", "real estate", "tax", "insurance", "retirement",
    "passive income", "money", "financial", "budget", "return", "portfolio",
}

_AI_TOOLS_TERMS = {
    "ai tool", "new tool", "launch", "software", "productivity", "automation",
    "chatgpt", "openai", "anthropic", "claude", "gemini", "llm",
    "ai assistant", "ai platform", "ai feature", "model release", "plugin",
}


class HealthWealthAIScraper(BaseScraper):
    def scrape(self) -> List[Dict[str, Any]]:
        all_items: List[Dict[str, Any]] = []

        for url, source in _HEALTH_SOURCES:
            raw = parse_rss_feed(url, source, "health_wealth_ai", max_items=8)
            filtered = [
                item for item in raw
                if any(kw in item["title"].lower() or kw in item["summary"].lower()
                       for kw in _HEALTH_TERMS)
            ]
            all_items.extend(filtered)

        for url, source in _WEALTH_SOURCES:
            raw = parse_rss_feed(url, source, "health_wealth_ai", max_items=8)
            filtered = [
                item for item in raw
                if any(kw in item["title"].lower() or kw in item["summary"].lower()
                       for kw in _WEALTH_TERMS)
            ]
            all_items.extend(filtered)

        for url, source in _AI_TOOLS_SOURCES:
            raw = parse_rss_feed(url, source, "health_wealth_ai", max_items=8)
            filtered = [
                item for item in raw
                if any(kw in item["title"].lower() or kw in item["summary"].lower()
                       for kw in _AI_TOOLS_TERMS)
            ]
            all_items.extend(filtered)

        return all_items
