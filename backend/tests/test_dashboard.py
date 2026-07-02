from backend.app.models.user import UserRole
from backend.app.models.dataset import Dataset, DatasetStatus
from backend.app.models.insight import AIInsight, InsightType
from backend.app.models.activity import ActivityLog
from backend.app.crud.user import user_repository
from backend.app.schemas.user import UserCreate


def test_dashboard_endpoint_requires_auth(client):
    """Tests that accessing the dashboard without a JWT token returns unauthorized"""
    response = client.get("/api/v1/dashboard")
    assert response.status_code == 401


def test_dashboard_empty_data(client, db):
    """Tests dashboard calculations when there is no data in the database"""
    # Create user and login
    user_in = UserCreate(
        email="dashuser@example.com",
        full_name="Dash User",
        password="password123",
        role=UserRole.BUSINESS_USER
    )
    user = user_repository.create(db, obj_in=user_in)

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "dashuser@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch dashboard
    response = client.get("/api/v1/dashboard", headers=headers)
    assert response.status_code == 200
    data = response.json()

    # Verify initial KPIs are all zero
    assert data["kpis"]["total_uploads"] == 0
    assert data["kpis"]["processed_datasets"] == 0
    assert data["kpis"]["active_insights"] == 0
    assert data["kpis"]["storage_used_bytes"] == 0
    assert len(data["upload_status"]) == 0
    assert len(data["insights"]) == 0
    assert len(data["recent_activities"]) == 0


def test_dashboard_with_aggregated_data(client, db):
    """Tests dashboard calculations and responses with populated datasets, insights, and activities"""
    # 1. Create user and login
    user_in = UserCreate(
        email="dashuser2@example.com",
        full_name="Dashboard User Two",
        password="password123",
        role=UserRole.BUSINESS_USER
    )
    user = user_repository.create(db, obj_in=user_in)

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "dashuser2@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Populate Datasets
    dataset1 = Dataset(
        name="sales_data.csv",
        file_type="csv",
        file_size=1024,
        status=DatasetStatus.COMPLETED,
        row_count=100,
        user_id=user.id
    )
    dataset2 = Dataset(
        name="customer_leads.xlsx",
        file_type="xlsx",
        file_size=2048,
        status=DatasetStatus.PROCESSING,
        user_id=user.id
    )
    dataset3 = Dataset(
        name="failed_log.txt",
        file_type="txt",
        file_size=512,
        status=DatasetStatus.FAILED,
        user_id=user.id
    )
    db.add_all([dataset1, dataset2, dataset3])

    # 3. Populate AI Insights
    insight1 = AIInsight(
        title="Q2 Sales Surge",
        content="AI analysis detected a 15% increase in product sales during Q2.",
        insight_type=InsightType.TREND,
        user_id=user.id
    )
    insight2 = AIInsight(
        title="Outlier Lead Detection",
        content="Detected 3 high-volume lead records that look anomalous.",
        insight_type=InsightType.ANOMALY,
        user_id=user.id
    )
    db.add_all([insight1, insight2])

    # 4. Populate Activity Logs
    activity1 = ActivityLog(
        user_id=user.id,
        action="file_upload",
        details="Uploaded sales_data.csv"
    )
    activity2 = ActivityLog(
        user_id=user.id,
        action="anomaly_detection",
        details="Ran lead outlier scan"
    )
    db.add_all([activity1, activity2])
    db.commit()

    # 5. Retrieve and Assert Dashboard Results
    response = client.get("/api/v1/dashboard", headers=headers)
    assert response.status_code == 200
    data = response.json()

    # KPI Checks
    # total_uploads = 3 files
    assert data["kpis"]["total_uploads"] == 3
    # processed_datasets = 1 file (dataset1 status = COMPLETED)
    assert data["kpis"]["processed_datasets"] == 1
    # active_insights = 2 insights
    assert data["kpis"]["active_insights"] == 2
    # storage_used_bytes = 1024 + 2048 + 512 = 3584
    assert data["kpis"]["storage_used_bytes"] == 3584

    # Uploads list checks (verify we get files ordered by latest first)
    assert len(data["upload_status"]) == 3
    assert data["upload_status"][0]["name"] == "failed_log.txt"
    assert data["upload_status"][1]["name"] == "customer_leads.xlsx"
    assert data["upload_status"][2]["name"] == "sales_data.csv"

    # Insights list checks
    assert len(data["insights"]) == 2
    assert data["insights"][0]["title"] == "Outlier Lead Detection"

    # Activity list checks
    assert len(data["recent_activities"]) == 2
    assert data["recent_activities"][0]["user_name"] == "Dashboard User Two"
    assert data["recent_activities"][0]["action"] == "anomaly_detection"
    assert data["recent_activities"][1]["action"] == "file_upload"
