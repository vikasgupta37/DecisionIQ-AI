from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.api import deps
from backend.app.crud.dashboard import dashboard_repository
from backend.app.schemas.dashboard import DashboardResponse

router = APIRouter()


@router.get("", response_model=DashboardResponse)
def get_dashboard_summary(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieves the consolidated dashboard metrics for the platform.
    Consists of KPI cards, recent data upload statuses, 
    latest AI-generated insights, and recent user/system audit activities.
    """
    kpis = dashboard_repository.get_kpis(db)
    uploads = dashboard_repository.get_recent_uploads(db)
    insights = dashboard_repository.get_recent_insights(db)
    activities = dashboard_repository.get_recent_activities(db)
    
    return DashboardResponse(
        kpis=kpis,
        upload_status=uploads,
        insights=insights,
        recent_activities=activities,
    )
