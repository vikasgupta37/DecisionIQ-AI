from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from backend.app.models.insight import InsightType
from backend.app.models.dataset import DatasetStatus


class KPICards(BaseModel):
    total_uploads: int
    processed_datasets: int
    active_insights: int
    storage_used_bytes: int


class UploadStatusItem(BaseModel):
    id: int
    name: str
    file_type: str
    file_size: int
    status: DatasetStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AIInsightItem(BaseModel):
    id: int
    title: str
    content: str
    insight_type: InsightType
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecentActivityItem(BaseModel):
    id: int
    user_name: str
    action: str
    details: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardResponse(BaseModel):
    kpis: KPICards
    upload_status: List[UploadStatusItem]
    insights: List[AIInsightItem]
    recent_activities: List[RecentActivityItem]
