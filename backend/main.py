import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from database import init_db
    from scheduler import setup_scheduler

    init_db()
    logger.info("Database initialised.")

    scheduler = setup_scheduler()
    scheduler.start()
    logger.info("Scheduler started.")

    yield

    scheduler.shutdown(wait=False)
    logger.info("Scheduler stopped.")


app = FastAPI(
    title="Daily Executive Intelligence Dashboard",
    version="1.0.0",
    lifespan=lifespan,
)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routes import router   # noqa: E402
app.include_router(router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("DASHBOARD_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False, log_level="info")
