import os
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/dashboard.db")

# SQLite needs check_same_thread=False; PostgreSQL doesn't accept that arg
if DATABASE_URL.startswith("sqlite"):
    pathlib.Path("data").mkdir(exist_ok=True)
    connect_args = {"check_same_thread": False}
else:
    # Render injects postgres:// but SQLAlchemy needs postgresql://
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    connect_args = {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    import models  # noqa: F401 — registers models on Base
    Base.metadata.create_all(bind=engine)
