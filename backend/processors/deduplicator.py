import difflib
from typing import List, Dict, Any

SIMILARITY_THRESHOLD = 0.75


def _sim(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()


def deduplicate(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    unique: List[Dict[str, Any]] = []
    for article in articles:
        title = article.get("title", "")
        duplicate_of = None
        for i, existing in enumerate(unique):
            if _sim(title, existing.get("title", "")) >= SIMILARITY_THRESHOLD:
                duplicate_of = i
                break
        if duplicate_of is None:
            unique.append(article)
        elif article.get("score", 0) > unique[duplicate_of].get("score", 0):
            unique[duplicate_of] = article
    return unique
