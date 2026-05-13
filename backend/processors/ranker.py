from datetime import datetime, timezone
from typing import List, Dict, Any

# Authority score per source name (0-1)
_SOURCE_AUTHORITY: Dict[str, float] = {
    "BBC World": 0.95,
    "The Guardian": 0.90,
    "Al Jazeera": 0.85,
    "Reuters": 0.95,
    "AP News": 0.90,
    "The Hindu": 0.95,
    "Indian Express": 0.90,
    "Economic Times": 0.88,
    "Hindustan Times": 0.85,
    "The Hindu AP": 0.92,
    "New Indian Express AP": 0.85,
    "FreightWaves": 0.90,
    "MIT Technology Review": 0.93,
    "VentureBeat AI": 0.88,
    "TechCrunch AI": 0.87,
    "Wired AI": 0.87,
    "GConnect": 0.85,
    "India Post": 0.90,
    "eGazette India": 0.95,
    "Gazette Notification": 0.90,
    "Google Trends India": 0.70,
    "X / Twitter Trends India": 0.70,
    "Google News Viral": 0.80,
    "Google News Trending India": 0.80,
    "Mashable": 0.78,
    "TIME": 0.88,
    "Reddit World News": 0.75,
    "WHO": 0.95,
    "WebMD": 0.85,
    "Health News": 0.78,
    "Wealth & Finance": 0.78,
    "Moneycontrol": 0.85,
    "AI Tools News": 0.80,
    "VentureBeat AI": 0.88,
}

_CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "international": [
        "war", "conflict", "economy", "crisis", "summit", "trade",
        "nuclear", "election", "climate", "sanction", "diplomacy",
    ],
    "national": [
        "india", "government", "parliament", "supreme court", "budget",
        "gst", "railway", "policy", "ministry", "rupee", "judiciary",
    ],
    "andhra": [
        "andhra", "ap", "amaravati", "vizag", "vijayawada", "tdp",
        "ysrcp", "jagan", "naidu", "telugu", "irrigation",
    ],
    "logistics": [
        "freight", "shipping", "supply chain", "warehouse", "cargo",
        "port", "logistics", "container", "e-commerce", "rail",
    ],
    "gconnect": [
        "7th pay", "da", "dearness", "cghs", "ltc", "leave",
        "pension", "service rule", "central government", "employee",
    ],
    "indiapost": [
        "india post", "dak", "postal", "parcel", "postmaster",
        "ippb", "speed post", "philately", "niryat",
    ],
    "gazette": [
        "gazette", "notification", "circular", "dopt", "india post",
        "recruitment", "promotion", "cadre", "deputation", "pension",
    ],
    "google_trends": [],
    "twitter_trends": [],
    "ai": [
        "ai", "llm", "gpt", "model", "neural", "robot", "automation",
        "generative", "openai", "anthropic", "deepmind", "agent",
    ],
    "viral_news": [
        "viral", "trending", "popular", "sensation", "goes viral",
        "most read", "breaking", "shocking", "world record", "extraordinary",
    ],
    "health_wealth_ai": [
        "health", "wellness", "fitness", "medical", "wealth", "investment",
        "finance", "savings", "ai tool", "new tool", "launch", "productivity",
        "mental health", "nutrition", "portfolio", "passive income",
    ],
}

_ALERT_MAP: Dict[str, List[str]] = {
    "critical": [
        "war", "attack", "disaster", "emergency", "ban", "collapse",
        "crisis", "explosion", "terror", "earthquake", "flood",
    ],
    "important": [
        "election", "verdict", "policy", "budget", "strike", "protest",
        "launch", "release", "notification", "circular", "gazette",
    ],
    "positive": [
        "growth", "record", "achievement", "award", "breakthrough",
        "success", "approved", "historic", "milestone",
    ],
}


def _freshness(published_at: datetime) -> float:
    if published_at.tzinfo is None:
        published_at = published_at.replace(tzinfo=timezone.utc)
    age_hours = (datetime.now(timezone.utc) - published_at).total_seconds() / 3600
    if age_hours <= 2:
        return 1.0
    if age_hours <= 6:
        return 0.85
    if age_hours <= 12:
        return 0.70
    if age_hours <= 24:
        return 0.50
    return 0.25


def _keyword_hit(title: str, summary: str, category: str) -> float:
    text = (title + " " + summary).lower()
    keywords = _CATEGORY_KEYWORDS.get(category, [])
    if not keywords:
        return 0.5
    hits = sum(1 for kw in keywords if kw in text)
    return min(hits / max(len(keywords) * 0.3, 1), 1.0)


def determine_alert_level(title: str, summary: str) -> str:
    text = (title + " " + summary).lower()
    for level, words in _ALERT_MAP.items():
        if any(w in text for w in words):
            return level
    return "none"


def score_article(article: Dict[str, Any]) -> float:
    authority = _SOURCE_AUTHORITY.get(article.get("source", ""), 0.70)
    freshness = _freshness(article.get("published_at", datetime.now(timezone.utc)))
    keyword = _keyword_hit(article.get("title", ""), article.get("summary", ""), article.get("category", ""))
    length_ok = 1.0 if len(article.get("title", "")) >= 20 else 0.80
    return round(0.35 * freshness + 0.30 * authority + 0.25 * keyword + 0.10 * length_ok, 4)


def rank_articles(articles: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
    for a in articles:
        a["score"] = score_article(a)
        a["alert_level"] = determine_alert_level(a.get("title", ""), a.get("summary", ""))
    articles.sort(key=lambda x: x["score"], reverse=True)
    return articles[:top_n]
