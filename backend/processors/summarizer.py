import re
import logging
from typing import Optional

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
MAX_WORDS = 35


def _strip_html(text: str) -> str:
    return BeautifulSoup(text, "html.parser").get_text(separator=" ").strip()


def _truncate(text: str, max_words: int = MAX_WORDS) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "…"


def _first_sentence(text: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return sentences[0].strip() if sentences else text.strip()


def summarize_article(title: str, description: str) -> str:
    if not description:
        return _truncate(title)

    clean = _strip_html(description)

    # If description is already short, use it directly
    if len(clean.split()) <= MAX_WORDS:
        return clean

    # Try sumy LSA summarizer
    try:
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lsa import LsaSummarizer
        from sumy.nlp.stemmers import Stemmer
        from sumy.utils import get_stop_words

        parser = PlaintextParser.from_string(clean, Tokenizer("english"))
        stemmer = Stemmer("english")
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")

        sentences = summarizer(parser.document, 2)
        result = " ".join(str(s) for s in sentences).strip()
        if result:
            return _truncate(result)
    except Exception as exc:
        logger.debug(f"sumy unavailable ({exc}); using first-sentence fallback")

    # Fallback: first sentence
    return _truncate(_first_sentence(clean))
