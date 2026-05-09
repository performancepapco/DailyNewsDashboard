import logging
import feedparser
from datetime import datetime, timezone
from typing import List, Dict, Any

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def parse_rss_feed(url: str, source_name: str, category: str, max_items: int = 10) -> List[Dict[str, Any]]:
    try:
        feed = feedparser.parse(url)
        items = []

        for entry in feed.entries[:max_items]:
            # Parse publish time
            published_at = datetime.now(timezone.utc)
            for attr in ("published_parsed", "updated_parsed"):
                t = getattr(entry, attr, None)
                if t:
                    try:
                        published_at = datetime(*t[:6], tzinfo=timezone.utc)
                        break
                    except Exception:
                        pass

            # Extract and clean summary
            raw_summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
            if raw_summary:
                raw_summary = BeautifulSoup(raw_summary, "html.parser").get_text(separator=" ").strip()

            title = (getattr(entry, "title", "") or "").strip()
            url_link = getattr(entry, "link", "") or ""

            if not title:
                continue

            items.append(
                {
                    "category": category,
                    "title": title,
                    "summary": raw_summary[:600],
                    "source": source_name,
                    "url": url_link,
                    "published_at": published_at,
                    "alert_level": "none",
                }
            )

        return items

    except Exception as exc:
        logger.error(f"RSS parse failed for {url}: {exc}")
        return []
