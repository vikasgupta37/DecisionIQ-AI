from typing import List, Tuple
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from backend.app.models.dataset import Dataset, DatasetStatus
from backend.app.models.insight import AIInsight
from backend.app.models.activity import ActivityLog
from backend.app.models.user import User
from backend.app.schemas.dashboard import KPICards, UploadStatusItem, AIInsightItem, RecentActivityItem


class DashboardRepository:
    def get_kpis(self, db: Session) -> KPICards:
        """
        Aggregates statistical KPI metrics across tables.
        """
        # Count total uploads
        total_uploads = db.scalar(select(func.count(Dataset.id))) or 0
        
        # Count processed completed datasets
        processed_datasets = db.scalar(
            select(func.count(Dataset.id)).where(Dataset.status == DatasetStatus.COMPLETED)
        ) or 0
        
        # Count total active insights
        active_insights = db.scalar(select(func.count(AIInsight.id))) or 0
        
        # Sum file sizes (coalesce to 0 if no files uploaded yet)
        storage_used_bytes = db.scalar(select(func.coalesce(func.sum(Dataset.file_size), 0))) or 0
        
        return KPICards(
            total_uploads=total_uploads,
            processed_datasets=processed_datasets,
            active_insights=active_insights,
            storage_used_bytes=storage_used_bytes,
        )

    def get_recent_uploads(self, db: Session, limit: int = 5) -> List[UploadStatusItem]:
        """
        Retrieves the latest dataset uploads.
        """
        stmt = select(Dataset).order_by(Dataset.created_at.desc(), Dataset.id.desc()).limit(limit)
        results = db.scalars(stmt).all()
        return [UploadStatusItem.model_validate(r) for r in results]

    def get_recent_insights(self, db: Session, limit: int = 5) -> List[AIInsightItem]:
        """
        Retrieves the latest AI-generated business insights.
        """
        stmt = select(AIInsight).order_by(AIInsight.created_at.desc(), AIInsight.id.desc()).limit(limit)
        results = db.scalars(stmt).all()
        return [AIInsightItem.model_validate(r) for r in results]

    def get_recent_activities(self, db: Session, limit: int = 10) -> List[RecentActivityItem]:
        """
        Retrieves the latest system and user activities, joining with the User table 
        to capture descriptive names.
        """
        stmt = (
            select(ActivityLog, User.full_name)
            .join(User, ActivityLog.user_id == User.id)
            .order_by(ActivityLog.created_at.desc(), ActivityLog.id.desc())
            .limit(limit)
        )
        
        results = db.execute(stmt).all()
        
        activities = []
        for log, full_name in results:
            activities.append(
                RecentActivityItem(
                    id=log.id,
                    user_name=full_name or "System User",
                    action=log.action,
                    details=log.details,
                    created_at=log.created_at,
                )
            )
        return activities

    def log_activity(self, db: Session, user_id: int, action: str, details: str = None) -> ActivityLog:
        """
        Helper method to create a new activity audit log record.
        """
        log = ActivityLog(user_id=user_id, action=action, details=details)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log


dashboard_repository = DashboardRepository()
