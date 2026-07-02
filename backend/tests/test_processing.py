import io
import json
import os
import shutil
from backend.app.crud.user import user_repository
from backend.app.models.user import UserRole
from backend.app.schemas.user import UserCreate
from backend.app.models.dataset import DatasetStatus


def _create_user_and_get_token(client, db, email="processor@example.com"):
    """Helper to create a user and return the JWT token."""
    user_in = UserCreate(
        email=email,
        full_name="Processor Tester",
        password="password123",
        role=UserRole.BUSINESS_USER,
    )
    user = user_repository.create(db, obj_in=user_in)
    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    return user, {"Authorization": f"Bearer {token}"}


def _cleanup_uploads():
    """Removes the uploads directory created during tests."""
    if os.path.exists("uploads"):
        shutil.rmtree("uploads")


def test_processing_requires_auth(client):
    """Triggering processing without a JWT token must return 401."""
    response = client.post("/api/v1/processing/1")
    assert response.status_code == 401


def test_process_csv_success(client, db):
    """Tests successful CSV file processing (de-duplication, null handling, stats)."""
    user, headers = _create_user_and_get_token(client, db)

    # 1. Upload a CSV with duplicate rows and null values
    csv_content = (
        b"name,age,income\n"
        b"Alice,30,50000\n"
        b"Bob,,60000\n"
        b"Alice,30,50000\n"  # Duplicate row
        b"Charlie,35,nan\n"  # Null income
        b"Dave,40,70000\n"
    )
    upload_resp = client.post(
        "/api/v1/upload",
        files={"file": ("dirty_data.csv", io.BytesIO(csv_content), "text/csv")},
        headers=headers,
    )
    assert upload_resp.status_code == 201
    dataset_id = upload_resp.json()["dataset"]["id"]

    # 2. Trigger processing
    response = client.post(f"/api/v1/processing/{dataset_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert data["dataset_id"] == dataset_id
    assert data["status"] == "completed"
    assert data["original_row_count"] == 5
    assert data["duplicates_removed"] == 1
    assert data["cleaned_row_count"] == 4
    assert data["nulls_filled"] == 2  # Bob's age, Charlie's income
    
    # 3. Quality report assertion
    assert data["quality_report"]["completeness"] > 0
    assert data["quality_report"]["total_duplicates"] == 1
    assert data["quality_report"]["total_nulls"] == 2

    # 4. Column statistics assertion
    col_names = [c["name"] for c in data["column_stats"]]
    assert "name" in col_names
    assert "age" in col_names
    assert "income" in col_names

    # Age column stats (should be detected as numeric or string depending on N/A proportion)
    # Bob has empty age, Charlie has 35, Alice has 30, Dave has 40. Values: '30', 'N/A', '35', '40'. 3 numeric values out of 4 non-null. So it is numeric.
    age_stat = next(c for c in data["column_stats"] if c["name"] == "age")
    assert age_stat["dtype"] == "numeric"
    assert age_stat["min"] == 30.0
    assert age_stat["max"] == 40.0

    # 5. Fetch report via GET
    report_resp = client.get(f"/api/v1/processing/{dataset_id}/report", headers=headers)
    assert report_resp.status_code == 200
    report_data = report_resp.json()
    assert report_data["dataset_id"] == dataset_id
    assert report_data["cleaned_row_count"] == 4

    _cleanup_uploads()


def test_process_json_success(client, db):
    """Tests successful JSON processing."""
    _, headers = _create_user_and_get_token(client, db, email="json_proc@example.com")

    json_data = [
        {"item": "A", "val": 10},
        {"item": "B", "val": 20},
        {"item": "A", "val": 10}, # Duplicate
    ]
    json_bytes = json.dumps(json_data).encode("utf-8")
    upload_resp = client.post(
        "/api/v1/upload",
        files={"file": ("items.json", io.BytesIO(json_bytes), "application/json")},
        headers=headers,
    )
    dataset_id = upload_resp.json()["dataset"]["id"]

    response = client.post(f"/api/v1/processing/{dataset_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()

    assert data["original_row_count"] == 3
    assert data["duplicates_removed"] == 1
    assert data["cleaned_row_count"] == 2

    _cleanup_uploads()


def test_process_unsupported_type_fails(client, db):
    """Tests that triggering processing on an unprocessable file type (like PDF) returns 400."""
    _, headers = _create_user_and_get_token(client, db, email="pdf_proc@example.com")

    # We mock upload a PDF file (we can't run full tabular processing on PDF)
    upload_resp = client.post(
        "/api/v1/upload",
        files={"file": ("doc.pdf", io.BytesIO(b"PDF-1.4..."), "application/pdf")},
        headers=headers,
    )
    dataset_id = upload_resp.json()["dataset"]["id"]

    response = client.post(f"/api/v1/processing/{dataset_id}", headers=headers)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "UNPROCESSABLE_TYPE"

    _cleanup_uploads()


def test_process_not_found_fails(client, db):
    """Tests that processing a non-existent dataset returns 404."""
    _, headers = _create_user_and_get_token(client, db, email="notfound_proc@example.com")
    response = client.post("/api/v1/processing/9999", headers=headers)
    assert response.status_code == 404


def test_get_report_not_found_fails(client, db):
    """Tests that requesting a non-existent processing report returns 404."""
    _, headers = _create_user_and_get_token(client, db, email="notfound_report@example.com")
    response = client.get("/api/v1/processing/9999/report", headers=headers)
    assert response.status_code == 404
