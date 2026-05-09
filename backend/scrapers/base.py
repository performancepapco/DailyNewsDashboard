import time
import logging
import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


class BaseScraper(ABC):
    MAX_RETRIES = 3
    BACKOFF_BASE = 2

    def fetch_url(self, url: str, timeout: int = 15) -> Optional[requests.Response]:
        for attempt in range(self.MAX_RETRIES):
            try:
                resp = requests.get(url, headers=HEADERS, timeout=timeout)
                resp.raise_for_status()
                return resp
            except requests.RequestException as exc:
                wait = self.BACKOFF_BASE ** attempt
                logger.warning(f"[{self.__class__.__name__}] attempt {attempt + 1} failed for {url}: {exc}. Retry in {wait}s")
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(wait)
        logger.error(f"[{self.__class__.__name__}] all {self.MAX_RETRIES} attempts failed for {url}")
        return None

    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        pass

    def run(self) -> List[Dict[str, Any]]:
        try:
            return self.scrape()
        except Exception as exc:
            logger.error(f"[{self.__class__.__name__}] run() failed: {exc}")
            return []
