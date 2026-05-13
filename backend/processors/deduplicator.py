import re
import difflib
from typing import List, Dict, Any
from urllib.parse import urlparse

# Within one scraper's results — catch near-identical titles from different feeds
_WITHIN_THRESHOLD = 0.80
# Across categories — stricter to avoid dropping genuinely different stories
_GLOBAL_THRESHOLD = 0.88

_STOP = {
    "the", "a", "an", "is", "in", "on", "at", "to", "of", "and", "or",
    "for", "with", "by", "from", "its", "it", "as", "be", "was", "are",
    "has", "have", "had", "that", "this", "says", "said", "will", "new",
}


def _norm_url(url: str) -> str:
    try:
        p = urlparse(url)
        return f"{p.scheme}://{p.netloc}{p.path}".rstrip("/").lower()
    except Exception:
        return url.lower()


def _kw(title: str) -> set:
    return {w for w in re.findall(r'\b[a-z]{4,}\b', title.lower()) if w not in _STOP}


def _sim(a: str, b: str) -> float:
    """Keyword overlap / max-set similarity (Jaccard variant)."""
    wa, wb = _kw(a), _kw(b)
    if not wa or not wb:
        return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()
    return len(wa & wb) / max(len(wa), len(wb))


def deduplicate(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Within-category dedup. Scores must be set before calling so that the
    most authoritative source wins when two articles cover the same story."""
    seen_urls: set = set()
    unique: List[Dict[str, Any]] = []

    for art in articles:
        url = _norm_url(art.get("url", ""))
        title = art.get("title", "")
        score = art.get("score", 0.0)

        # ── Exact URL collision → keep higher-scored version ──
        if url and url in seen_urls:
            for i, u in enumerate(unique):
                if _norm_url(u.get("url", "")) == url:
                    if score > u.get("score", 0.0):
                        unique[i] = art
                    break
            continue

        # ── Title similarity collision → keep higher-scored version ──
        dup_idx = None
        for i, ex in enumerate(unique):
            if _sim(title, ex.get("title", "")) >= _WITHIN_THRESHOLD:
                dup_idx = i
                break

        if dup_idx is None:
            if url:
                seen_urls.add(url)
            unique.append(art)
        elif score > unique[dup_idx].get("score", 0.0):
            seen_urls.discard(_norm_url(unique[dup_idx].get("url", "")))
            if url:
                seen_urls.add(url)
            unique[dup_idx] = art

    return unique


def global_deduplicate(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Cross-category dedup. Call after all scrapers have run and articles are
    pre-scored. Processes highest-scored first so the best version of each story
    is kept and lower-quality duplicates in other categories are dropped."""
    seen_urls: set = set()
    unique: List[Dict[str, Any]] = []

    for art in sorted(articles, key=lambda x: x.get("score", 0.0), reverse=True):
        url = _norm_url(art.get("url", ""))
        title = art.get("title", "")

        if url and url in seen_urls:
            continue

        if any(_sim(title, u.get("title", "")) >= _GLOBAL_THRESHOLD for u in unique):
            continue

        if url:
            seen_urls.add(url)
        unique.append(art)

    return unique
