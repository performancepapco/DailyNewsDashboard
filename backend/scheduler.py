import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)


def _run_refresh():
    from api.routes import trigger_refresh
    logger.info("APScheduler: starting daily refresh (09:00 AM IST)")
    count = trigger_refresh()
    logger.info(f"APScheduler: daily refresh complete — {count} articles stored")


def setup_scheduler() -> BackgroundScheduler:
    # 09:00 AM IST = 03:30 UTC
    scheduler = BackgroundScheduler(timezone="UTC", misfire_grace_time=3600)
    scheduler.add_job(
        _run_refresh,
        CronTrigger(hour=3, minute=30, timezone="UTC"),
        id="daily_refresh",
        replace_existing=True,
    )
    logger.info("Scheduler configured: daily refresh at 03:30 UTC (09:00 AM IST)")
    return scheduler
