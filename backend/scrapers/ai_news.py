from typing import List, Dict, Any
from .base import BaseScraper
from .rss_scraper import parse_rss_feed

RSS_SOURCES = [
    ("https://venturebeat.com/category/ai/feed/", "VentureBeat AI"),
    ("https://techcrunch.com/tag/artificial-intelligence/feed/", "TechCrunch AI"),
    ("https://www.technologyreview.com/feed/", "MIT Technology Review"),
    ("https://www.wired.com/feed/tag/artificial-intelligence/rss", "Wired AI"),
    (
        "https://news.google.com/rss/search?q=artificial+intelligence+LLM+model+release"
        "+when:24h&hl=en&gl=US&ceid=US:en",
        "AI Research News",
    ),
]

_AI_TERMS = {
    "ai", "llm", "gpt", "model", "neural", "robot", "automation",
    "generative", "openai", "anthropic", "deepmind", "gemini", "claude",
    "mistral", "llama", "agent", "chatbot", "machine learning", "deep learning",
}


class AIScraper(BaseScraper):
    def scrape(self) -> List[Dict[str, Any]]:
        all_items: List[Dict[str, Any]] = []
        for url, source in RSS_SOURCES:
            raw = parse_rss_feed(url, source, "ai", max_items=10)
            # Keep only items that mention AI topics
            filtered = [
                item for item in raw
                if any(
                    kw in item["title"].lower() or kw in item["summary"].lower()
                    for kw in _AI_TERMS
                )
            ]
            all_items.extend(filtered)
        return all_items
