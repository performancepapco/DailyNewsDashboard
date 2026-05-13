import json
import logging
import pathlib
from datetime import date, datetime, timezone
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, get_db, DATABASE_URL
from models import Article, DailySnapshot
from schemas import ArticleOut, CategoryData, DashboardResponse, RefreshResponse
from processors.summarizer import summarize_article
from processors.ranker import rank_articles
from processors.deduplicator import deduplicate

router = APIRouter()
logger = logging.getLogger(__name__)

CATEGORIES = [
    "international", "national", "andhra", "logistics",
    "gconnect", "indiapost", "gazette",
    "google_trends", "twitter_trends", "ai",
    "viral_news", "health_wealth_ai",
]

ARCHIVE_DIR = pathlib.Path("data/archives")


# ── Internal helpers ────────────────────────────────────────────────────────

def _import_scrapers():
    from scrapers.international import InternationalScraper
    from scrapers.national import NationalScraper
    from scrapers.andhra import AndhraScraper
    from scrapers.logistics import LogisticsScraper
    from scrapers.gconnect import GConnectScraper
    from scrapers.indiapost import IndiaPostScraper
    from scrapers.gazette import GazetteScraper
    from scrapers.google_trends import GoogleTrendsScraper
    from scrapers.twitter_trends import TwitterTrendsScraper
    from scrapers.ai_news import AIScraper
    from scrapers.viral_news import ViralNewsScraper
    from scrapers.health_wealth_ai_tools import HealthWealthAIScraper

    return [
        InternationalScraper(), NationalScraper(), AndhraScraper(),
        LogisticsScraper(), GConnectScraper(), IndiaPostScraper(),
        GazetteScraper(), GoogleTrendsScraper(), TwitterTrendsScraper(),
        AIScraper(), ViralNewsScraper(), HealthWealthAIScraper(),
    ]


def _fetch_and_store(db: Session) -> int:
    today = date.today().isoformat()

    # Clear today's stale data
    db.query(Article).filter(Article.date_key == today).delete()
    db.commit()

    total = 0
    for scraper in _import_scrapers():
        try:
            raw = scraper.run()
            raw = deduplicate(raw)
            ranked = rank_articles(raw, top_n=getattr(scraper, "top_n", 5))

            for item in ranked:
                summary = summarize_article(item.get("title", ""), item.get("summary", ""))
                db.add(Article(
                    date_key=today,
                    category=item.get("category", ""),
                    title=item.get("title", "")[:500],
                    summary=summary[:300],
                    source=item.get("source", "")[:100],
                    url=item.get("url", "")[:1000],
                    published_at=item.get("published_at"),
                    score=item.get("score", 0.0),
                    alert_level=item.get("alert_level", "none"),
                ))
                total += 1

            db.commit()
            logger.info(f"{scraper.__class__.__name__}: saved {len(ranked)} articles")

        except Exception as exc:
            logger.error(f"{scraper.__class__.__name__} failed: {exc}")
            db.rollback()

    _save_snapshot(db, today, total)
    _cleanup_old_archives(db)
    return total


def _save_snapshot(db: Session, date_str: str, total: int) -> None:
    import os
    use_files = DATABASE_URL.startswith("sqlite")   # only write files locally

    json_path = ""
    if use_files:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        json_path = str(ARCHIVE_DIR / f"{date_str}.json")
        articles = db.query(Article).filter(Article.date_key == date_str).all()
        payload = [ArticleOut.model_validate(a).model_dump(mode="json") for a in articles]
        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2, default=str)

    snap = db.query(DailySnapshot).filter(DailySnapshot.date == date_str).first()
    if snap:
        snap.json_path = json_path
        snap.total_items = total
    else:
        db.add(DailySnapshot(date=date_str, json_path=json_path, total_items=total))
    db.commit()


def _cleanup_old_archives(db: Session) -> None:
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(days=90)).date().isoformat()
    old = db.query(DailySnapshot).filter(DailySnapshot.date < cutoff).all()
    for snap in old:
        try:
            pathlib.Path(snap.json_path).unlink(missing_ok=True)
        except Exception:
            pass
        db.delete(snap)
    db.commit()


def trigger_refresh() -> int:
    """Called by APScheduler — creates its own DB session."""
    db = SessionLocal()
    try:
        return _fetch_and_store(db)
    finally:
        db.close()


# ── API routes ───────────────────────────────────────────────────────────────

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    try:
        today = date.today().isoformat()
        articles = (
            db.query(Article)
            .filter(Article.date_key == today)
            .order_by(Article.score.desc())
            .all()
        )

        by_cat: dict = {c: [] for c in CATEGORIES}
        for a in articles:
            if a.category in by_cat:
                by_cat[a.category].append(ArticleOut.model_validate(a))

        snap = db.query(DailySnapshot).filter(DailySnapshot.date == today).first()
        # Append Z so browsers know the stored time is UTC and convert to local (IST) correctly
        last_refreshed = snap.created_at.isoformat() + "Z" if snap and snap.created_at else None

        return DashboardResponse(
            date=today,
            categories={c: CategoryData(name=c, articles=items) for c, items in by_cat.items()},
            total_items=len(articles),
            alerts=[ArticleOut.model_validate(a) for a in articles if a.alert_level in ("critical", "important")],
            gazette_count=len(by_cat.get("gazette", [])),
            ai_count=len(by_cat.get("ai", [])),
            last_refreshed=last_refreshed,
        )
    except Exception as exc:
        logger.error(f"Dashboard endpoint error: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/refresh", response_model=RefreshResponse)
def refresh(background_tasks: BackgroundTasks):
    background_tasks.add_task(trigger_refresh)
    return RefreshResponse(status="started", message="Full refresh triggered in background. Data will appear within 1–2 minutes.")


@router.get("/categories/{name}")
def get_category(name: str, db: Session = Depends(get_db)):
    if name not in CATEGORIES:
        raise HTTPException(status_code=404, detail=f"Unknown category: {name}")
    today = date.today().isoformat()
    articles = (
        db.query(Article)
        .filter(Article.date_key == today, Article.category == name)
        .order_by(Article.score.desc())
        .all()
    )
    return [ArticleOut.model_validate(a) for a in articles]


@router.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    today = date.today().isoformat()
    articles = (
        db.query(Article)
        .filter(
            Article.date_key == today,
            (Article.title.ilike(f"%{q}%") | Article.summary.ilike(f"%{q}%")),
        )
        .order_by(Article.score.desc())
        .all()
    )
    return [ArticleOut.model_validate(a) for a in articles]


@router.get("/archive")
def list_archives(db: Session = Depends(get_db)):
    snaps = db.query(DailySnapshot).order_by(DailySnapshot.date.desc()).all()
    return [{"date": s.date, "total_items": s.total_items} for s in snaps]


@router.get("/archive/{date_str}")
def get_archive(date_str: str, db: Session = Depends(get_db)):
    snap = db.query(DailySnapshot).filter(DailySnapshot.date == date_str).first()
    if not snap:
        raise HTTPException(status_code=404, detail="Archive not found")
    # Local: serve from JSON file; Cloud: query DB directly
    if snap.json_path:
        p = pathlib.Path(snap.json_path)
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    articles = db.query(Article).filter(Article.date_key == date_str).order_by(Article.score.desc()).all()
    return [ArticleOut.model_validate(a).model_dump(mode="json") for a in articles]


@router.get("/health")
def health():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@router.get("/db-status")
def db_status():
    """Diagnostic endpoint — checks DB connectivity and table existence."""
    import sqlalchemy
    try:
        db = SessionLocal()
        article_count = db.query(Article).count()
        snap_count = db.query(DailySnapshot).count()
        db.close()
        return {
            "status": "ok",
            "database_url_scheme": DATABASE_URL.split(":")[0],
            "article_count": article_count,
            "snapshot_count": snap_count,
        }
    except Exception as exc:
        return {
            "status": "error",
            "database_url_scheme": DATABASE_URL.split(":")[0],
            "error": str(exc),
        }
