from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional, Dict


class ArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_key: str
    category: str
    title: str
    summary: str
    source: str
    url: str
    published_at: Optional[datetime] = None
    score: float
    alert_level: str


class CategoryData(BaseModel):
    name: str
    articles: List[ArticleOut]


class DashboardResponse(BaseModel):
    date: str
    categories: Dict[str, CategoryData]
    total_items: int
    alerts: List[ArticleOut]
    gazette_count: int
    ai_count: int
    last_refreshed: Optional[str] = None


class RefreshResponse(BaseModel):
    status: str
    message: str
