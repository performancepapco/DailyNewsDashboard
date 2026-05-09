from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    date_key = Column(String(10), index=True)   # YYYY-MM-DD
    category = Column(String(50), index=True)
    title = Column(String(500))
    summary = Column(Text)
    source = Column(String(100))
    url = Column(String(1000))
    published_at = Column(DateTime(timezone=True))
    score = Column(Float, default=0.0)
    alert_level = Column(String(20), default="none")  # critical | important | positive | none
    created_at = Column(DateTime, server_default=func.now())


class DailySnapshot(Base):
    __tablename__ = "daily_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(10), unique=True, index=True)  # YYYY-MM-DD
    json_path = Column(String(500))
    total_items = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
